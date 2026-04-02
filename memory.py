import json
from config import MEMORY_FILE_PATH, MAX_MEMORY_ROUNDS

# 初始化默认记忆（空列表）
DEFAULT_MEMORY = []

def init_memory():
    """初始化记忆文件（首次运行创建）"""
    try:
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_memory(DEFAULT_MEMORY)

def load_memory():
    """加载最近的对话记忆"""
    init_memory()
    with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    """保存更新后的记忆"""
    with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def add_memory(user_input, ai_reply):
    """添加新的对话记忆，超过6轮则删除最早的"""
    memory = load_memory()
    # 追加新轮次对话
    memory.append({"user": user_input, "ai": ai_reply})
    # 只保留最近MAX_MEMORY_ROUNDS轮（6轮）
    if len(memory) > MAX_MEMORY_ROUNDS:
        memory = memory[-MAX_MEMORY_ROUNDS:]
    save_memory(memory)

def format_memory(memory):
    """格式化记忆为prompt可识别的文本（给agent模块用）"""
    if not memory:
        return "无"
    history = []
    for idx, round_data in enumerate(memory, 1):
        history.append(f"第{idx}轮：用户说{round_data['user']}，AI说{round_data['ai']}")
    return "\n".join(history)