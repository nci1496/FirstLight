import requests
import json
from config import OLLAMA_API_URL, OLLAMA_MODEL
from memory import format_memory

def build_prompt(state, memory, user_input):
    """拼接Prompt（严格按方案模板，动态填充参数）"""
    # 格式化对话记忆
    history_text = format_memory(memory)
    # 方案指定的核心Prompt模板，一字不改
    prompt_template = """你是一个陪伴型AI，不是工具。
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
请自然回复，不要解释自己是AI。"""
    # 动态填充参数
    prompt = prompt_template.format(
        emotion=state["emotion"],
        affection=state["affection"],
        history=history_text,
        input=user_input
    )
    return prompt

def call_llm(prompt):
    """调用Ollama本地模型API，获取AI回复"""
    # 构造Ollama请求参数
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,  # 非流式输出，极简版无需流式
        "temperature": 0.7  # 温度值，控制回复随机性
    }
    try:
        # 发送POST请求调用本地模型
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=30  # 超时时间30秒，防止本地模型加载慢
        )
        response.raise_for_status()  # 抛出HTTP请求错误
        # 解析返回结果
        result = response.json()
        return result.get("response", "我有点没理解你的意思～")
    except requests.exceptions.RequestException as e:
        # 异常处理，保证程序不崩溃
        print(f"模型调用失败：{e}")
        return "抱歉，我这边出了点小问题，暂时无法回复～"