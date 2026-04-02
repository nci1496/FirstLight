import json
from config import STATE_FILE_PATH

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

def update_state(user_input):
    """根据用户输入更新状态（写死基础规则，方案核心）"""
    state = load_state()
    # 规则1：用户说累/疲惫/倦 → 情绪变为关心，好感度+1
    if any(word in user_input for word in ["累", "疲惫", "倦", "乏"]):
        state["emotion"] = "caring"
        state["affection"] += 1
    # 规则2：用户说开心/高兴/快乐 → 情绪变为开心，好感度+1
    elif any(word in user_input for word in ["开心", "高兴", "快乐", "爽"]):
        state["emotion"] = "happy"
        state["affection"] += 1
    # 规则3：用户说烦/生气/讨厌 → 情绪变为冷淡，好感度-1
    elif any(word in user_input for word in ["烦", "生气", "讨厌", "烦"]):
        state["emotion"] = "cold"
        state["affection"] -= 1
    # 可根据需求扩展其他规则，核心保持极简
    save_state(state)