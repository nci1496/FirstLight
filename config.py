# 配置Ollama本地API地址
OLLAMA_API_URL = "http://localhost:11434/api/generate"
# 调用的本地模型（默认mistral，可替换为ollama支持的其他模型）
OLLAMA_MODEL = "mistral"

# 记忆和状态文件的持久化路径
MEMORY_FILE_PATH = "./data/memory.json"
STATE_FILE_PATH = "./data/state.json"

# 短期记忆最大轮数（暂时6轮）
MAX_MEMORY_ROUNDS = 6

AFFECTION_RANGE = (-2, 2)  # 好感度单次变化范围（按反馈要求）
VALID_EMOTIONS = ["neutral", "caring", "happy", "cold", "soft", "tired"]  # 合法情绪值
DEFAULT_REPLY = "我有点没跟上你的思路～"  # JSON解析失败兜底回复