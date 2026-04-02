from persona import load_state, update_state_by_llm
from memory import load_memory, add_memory
from agent import build_prompt, call_llm


def main():
    """项目入口，核心交互循环"""
    print("✨ AI陪伴助手已启动，输入任意内容开始聊天，输入'退出'结束对话 ✨")
    while True:
        # 1. 获取用户输入
        user_input = input("\n你: ").strip()
        if user_input in ["退出", "结束", "拜拜"]:
            print("她: 再见啦，下次再聊～")
            break
        if not user_input:
            print("她: 你好像没说什么哦，再说点吧～")
            continue

        # 2. 加载当前状态和记忆
        current_state = load_state()
        current_memory = load_memory()

        # 3. 拼接Prompt，调用本地模型
        prompt = build_prompt(current_state, current_memory, user_input)
        llm_data = call_llm(prompt)  # 升级：返回字典{reply, affection_change, emotion}

        # 4. 输出AI回复
        print(f"她: {llm_data['reply']}")

        # 5. 由LLM决策更新状态 + 保存新记忆（核心升级）
        update_state_by_llm(llm_data["affection_change"], llm_data["emotion"])
        add_memory(user_input, llm_data["reply"])


if __name__ == "__main__":
    main()