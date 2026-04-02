# FirstLight_MVP 技术文档

## 一、项目概述

基于Ollama+mistral本地模型实现的轻量陪伴型AI，支持本地聊天、6轮短期记忆、简单人格及状态动态变化，核心流程：输入→读状态→拼Prompt→调LLM→输出→更状态→存记忆。

## 二、文件结构及函数接口

### 1. config.py（全局配置）

- 作用：定义Ollama接口、文件路径、记忆最大轮数，统一配置便于修改

- 核心常量：OLLAMA_API_URL、OLLAMA_MODEL、MEMORY_FILE_PATH、STATE_FILE_PATH、MAX_MEMORY_ROUNDS
  
  ### 2. persona.py（人格/状态管理）

- 作用：实现状态的初始化、加载、保存及基于用户输入的更新，控制AI情绪和好感度

- init_state()：首次运行初始化状态文件，无入参/返回值

- load_state()：加载当前状态，无入参，返回状态字典{emotion, affection}

- save_state(state)：保存状态，入参为状态字典，无返回值（自动限制好感度0~100）

- update_state(user_input)：根据用户输入更新状态，入参为用户输入字符串，无返回值
  
  ### 3. memory.py（短期记忆管理）

- 作用：实现对话记忆的增删、持久化、格式化，仅保留最近6轮对话

- init_memory()：首次运行初始化记忆文件，无入参/返回值

- load_memory()：加载对话记忆，无入参，返回记忆列表

- save_memory(memory)：保存记忆，入参为记忆列表，无返回值

- add_memory(user_input, ai_reply)：添加新对话，入参为用户/AI输入字符串，无返回值（自动截断超量记忆）

- format_memory(memory)：格式化记忆为Prompt文本，入参为记忆列表，返回格式化字符串
  
  ### 4. agent.py（核心逻辑）

- 作用：Prompt拼接、Ollama本地模型API调用，为项目核心

- build_prompt(state, memory, user_input)：拼接Prompt，入参为状态字典、记忆列表、用户输入，返回拼接后的Prompt字符串

- call_llm(prompt)：调用Ollama模型，入参为Prompt字符串，返回AI回复字符串（含异常处理）
  
  ### 5. main.py（入口运行）

- 作用：实现人机交互主循环，串联所有模块执行核心流程

- main()：项目入口函数，无入参/返回值，实现输入获取、模块调用、输出及状态/记忆更新的循环
  
  ## 三、前置依赖
1. 环境：Ollama本地客户端+mistral模型（ollama run mistral）

2. Python依赖：requests（pip install requests）

3. 系统：Windows/macOS（需管理员权限安装Ollama）
   
   ## 四、后续改进方向

4. 扩展state更新规则，增加更多情绪/触发关键词

5. 支持流式输出，提升聊天交互体验

6. 增加长期记忆模块，区分短期/长期记忆

7. 优化Prompt模板，提升人格特征的辨识度

8. 增加状态回滚、记忆清空等手动操作接口

9. 支持多模型切换，可配置模型参数（温度、最大生成长度）

10. 增加异常监控，记录模型调用/文件操作错误日志
