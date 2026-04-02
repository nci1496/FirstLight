import json
from config import STATE_FILE_PATH, AFFECTION_RANGE, VALID_EMOTIONS

# 初始化默认状态
DEFAULT_STATE = {
    "emotion": "neutral",  # 情绪：neutral/happy/caring/tired/cold
    "affection": 50       # 好感度：0~100
}

def init_state():
    """初始化状态文件（首次运行创建）"""
    try:
        with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_state(DEFAULT_STATE)

def load_state():
    """加载当前状态"""
    init_state()
    with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    """保存更新后的状态"""
    # 限制好感度在0~100之间，防止溢出
    state["affection"] = max(0, min(100, state["affection"]))
    with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def update_state_by_llm(affection_change, new_emotion):
    """
    由LLM决策更新状态（核心升级）
    :param affection_change: LLM输出的好感度变化值
    :param new_emotion: LLM输出的新情绪值
    :return: 无
    """
    state = load_state()
    # 校验好感度变化值，超出范围则取边界
    ac = max(AFFECTION_RANGE[0], min(AFFECTION_RANGE[1], affection_change))
    state["affection"] += ac
    # 校验情绪值，非法则保留原情绪
    state["emotion"] = new_emotion if new_emotion in VALID_EMOTIONS else state["emotion"]
    save_state(state)