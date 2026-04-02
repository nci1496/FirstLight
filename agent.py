import requests
import json
from config import OLLAMA_API_URL, OLLAMA_MODEL, DEFAULT_REPLY, VALID_EMOTIONS, AFFECTION_RANGE
from memory import format_memory

def build_prompt(state, memory, user_input):
    """拼接Prompt（严格按方案模板，动态填充参数）"""
    # 格式化对话记忆
    history_text = format_memory(memory)
    # 方案指定的核心Prompt模板，一字不改
    prompt_template = """你是一个陪伴型AI搭档，不是工具，你的核心目标：
    1. 让用户状态变好
    2. 鼓励用户行动
    3. 避免让用户长期消极

    你的性格：
    - 稍微理性
    - 会关心人
    - 说话自然，不做作

    当前状态：
    - 情绪：{emotion}
    - 好感度：{affection}
    最近对话：
    {history}
    用户刚刚说：
    {input}

    【输出要求】
    必须严格返回JSON格式，无任何额外文字，JSON字段如下：
    - reply：对用户的自然回复，不解释自己是AI，符合当前情绪
    - affection_change：好感度变化值，整数，范围{aff_min}~{aff_max}
    - emotion：你的新情绪值，必须从列表[{emotions}]中选择

    示例输出：
    {{"reply":"辛苦啦，歇会儿吧～","affection_change":1,"emotion":"caring"}}"""
    # 动态填充参数
    prompt = prompt_template.format(
        emotion=state["emotion"],
        affection=state["affection"],
        history=history_text,
        input=user_input,
        aff_min=AFFECTION_RANGE[0],
        aff_max=AFFECTION_RANGE[1],
        emotions=",".join(VALID_EMOTIONS)
    )
    return prompt

def parse_llm_json(llm_output):
    """
    解析LLM输出的JSON字符串
    :param llm_output: LLM原始输出
    :return: 字典{reply, affection_change, emotion}，解析失败则返回兜底值
    """
    try:
        # 清洗可能的多余字符，仅保留JSON部分
        llm_output = llm_output.strip().replace("```json", "").replace("```", "")
        data = json.loads(llm_output)
        # 校验字段完整性
        required_fields = ["reply", "affection_change", "emotion"]
        if not all(f in data for f in required_fields):
            raise ValueError("缺少核心字段")
        # 类型转换（防止LLM输出非整数）
        data["affection_change"] = int(data["affection_change"])
        return data
    except Exception as e:
        # 所有异常都返回兜底值
        return {
            "reply": DEFAULT_REPLY,
            "affection_change": 0,
            "emotion": VALID_EMOTIONS[0]  # neutral
        }

def call_llm(prompt):
    """调用Ollama本地模型API，获取AI回复"""
    # 构造Ollama请求参数
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,  # 非流式输出，极简版无需流式
        "temperature": 0.7, # 温度值，控制回复随机性
        "stop": ["\n\n"]  # 防止LLM输出多余内容
    }
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        raw_output = response.json().get("response", "")
        # 解析JSON并返回
        return parse_llm_json(raw_output)
    except requests.exceptions.RequestException as e:
        print(f"模型调用失败：{e}")
        # 模型调用失败也返回兜底值
        return {
            "reply": "抱歉，我这边出了点小问题，暂时无法回复～",
            "affection_change": 0,
            "emotion": VALID_EMOTIONS[0]
        }