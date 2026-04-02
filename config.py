# 配置Ollama本地API地址（默认本地运行就是这个地址）
OLLAMA_API_URL = "http://localhost:11434/api/generate"
# 调用的本地模型（方案指定mistral，可替换为ollama支持的其他模型）
OLLAMA_MODEL = "mistral"

# 记忆和状态文件的持久化路径
MEMORY_FILE_PATH = "./data/memory.json"
STATE_FILE_PATH = "./data/state.json"

# 短期记忆最大轮数（方案指定6轮）
MAX_MEMORY_ROUNDS = 6