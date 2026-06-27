# Agent 开发框架设计文档


## 核心架构

# Agent IDE 项目结构

## 根目录

```

agent_exploit/
├── README.md
├── agents/
│   └── agents_login.json          # Agent 组注册表
├── desmake/                        # 🔧 工具暂存区
│   ├── desmake.py                  # 工具注册程序
│   └── add/
│       └── ++main++.py             # 待注册工具示例
└── server/                         # 🌐 Go Web 服务器
    ├── first.go                    # 入口
    ├── go.mod / go.sum
    ├── router/
    │   └── router.go               # 路由注册
    └── web_handle_func/            # 页面 & 处理函数
        ├── web_handle_func.go      # 路由处理函数
        ├── HomePage.html           # 首页
        ├── OperatePage.html        # 组管理页面
        ├── OperatePage_single.html # 组内操作页面
        ├── OperatePage_single_single.html # 单个Agent页面
        └── AgentCorresspondPage.html     # 通信页面


## 🐍 Python Agent 框架 (agent_frame/)

agent_frame/
├── agent_login.json             # Agent 注册表
├── agent_queue.py               # 共享消息队列
├── call_stucture.json           # 消息打包结构规范
├── generate.py                  # Agent 生成程序
├── main.py                      # 主通信程序（预热所有Agent）
│
├── 🔧 三大核心类
├── ai_clone_class/
│   ├── ai_clone.py              # Agent 主体类
│   ├── ai_des.py                # 工具描述类
│   └── ai_tools.py              # 工具类
│
├── 🏭 生成模块
├── ai_generate/
│   ├── ai_generate.py           # 新Agent生成接口
│   └── new_ai/                  # Agent 模板
│       ├── ai_self.py
│       ├── memory.py / memory.txt / memoryed.txt
│       ├── role.txt
│       └── ai_tools/
│           ├── des/             # 工具描述文件夹
│           └── tools/           # 工具文件夹
│               └── 工具名/
│                   └── ++main++ # ⚡ 工具唯一入口
│
├── 🧠 记忆概括 Agent
├── memory_ai/
│   ├── ai_self.py / memory.py / role.txt ...
│   └── ai_tools/tools/megeneral/
│       └── ++main++.py
│
├── 📝 工具描述 Agent
├── tools_make_ai/
│   ├── ai_self.py / role.txt ...
│   └── ai_tools/tools/tools_make/
│       └── ++main++.py
│
└── 📡 接口层
    └── port/
        ├── desmake_port.py      # 工具注册接口
        └── memory_port.py       # 记忆概括接口

```


## 三大核心类

| 类 | 作用 | 位置 |
|----|------|------|
| ai_clone | Agent 初始化与运行程序 | 各组内 |
| ai_des | Agent 工具函数描述 | 各组内 |
| ai_tools | Agent 工具函数 | 各组内 |

初始为空，Agent 实例化后读取记忆、人设、工具描述文件、工具文件组装。


## Agent 文件结构规范

| 文件 | 格式 | 说明 |
|------|------|------|
| role.txt | 纯文本 | 人设 |
| memory.txt | 纯文本 | 记忆 |
| tools/tool_des.json | JSON | 工具描述 |
| tools/工具名/++main++ | Python | 工具唯一入口文件 |

每个 Agent 文件夹名 = 唯一标识，路径隔离。


## 工具制作规范

1. 除标准库外，其余导入必须在函数内部
2. 工具不能修改工具文件夹外的文件，只能读
3. 文件夹名称 = 工具函数名称，必须统一
4. 只读取 ++main++ 文件作为工具入口


## 内置 Agent

| Agent | 作用 |
|-------|------|
| 记忆 Agent | 记忆概括精简 |
| 工具注册 Agent | 为写好的工具生成描述 |


## 接口程序

| 程序 | 位置 | 作用 |
|------|------|------|
| generate.py | 根目录 | 创建/删除 Agent |
| desmake.py | tools 文件夹 | 注册/修改/删除工具描述 |
| memory.py | Agent 主目录 | 调用记忆 Agent |


## 启动与注册

| 文件 | 作用 |
|------|------|
| agent_login / agents_login.json | 注册所有 Agent /Agents组 |
| main.py | 入口，预加载所有 Agent |


## 通信机制（类计算机网络）

每个 Agent：
  - 收件箱（inbox/）
  - 发件箱（outbox/）
  - 共享消息队列

流程：
  Agent 返回结构化文本
  → 代码解析打包
  → 放入发件箱
  → 放入共享队列
  → 接线员解析转发
  → 目标 Agent 收件箱 或 user 或 all

接线员、Agent 都是并发持续扫描。


## 调用流程规范

| 结构 | 作用 |
|------|------|
| agent_call_queue | 中心 Agent 规划流程后发送到此 |
| call_structure | 规划好的流程格式规范 |


## 设计思想

驱动和 Agent 信息分离，Agent 存储调用结构统一。

- 工具不通用，每个 Agent 有自己的工具
- 文件夹名称作为唯一标识，路径分割，隔离管理
- 动态导入，无侵入


## 后端服务接口

### 页面路由

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 首页 |
| GET | /OperatePage | 总操作页面（Agent组管理） |
| GET | /OperatePage_single | Agent组内操作页面 |
| GET | /OperatePage_single_single | 单个Agent操作页面 |
| GET | /AgentCorresspondPage | Agent通信页面 |


### 对所有Agent组操作

| 方法 | 路径 | 说明 | 请求参数 |
|------|------|------|----------|
| GET | /api/agents/List | 列出所有Agent组 | 无 |
| POST | /api/agents/Creat | 创建Agent组 | Name: 组名称 |
| POST | /api/agents/Delete | 删除Agent组 | Name: 组名称 |
| POST | /api/agents/Change | 修改Agent组名 | OldName: 旧名, NewName: 新名 |


### 一个Agent组内操作

| 方法 | 路径 | 说明 | 请求参数 |
|------|------|------|----------|
| POST | /api/agentsingle/List | 列出组内所有Agent | Name: 组名称 |
| POST | /api/agentsingle/Creat | 创建Agent | Name: 组名称, NewAgentName: Agent名, Role: 人设 |
| POST | /api/agentsingle/Delete | 删除Agent | Name: 组名称, AgentName: Agent名 |


### 一个Agent内操作

| 方法 | 路径 | 说明 | 请求参数 |
|------|------|------|----------|
| POST | /api/agentsingle_single/RoleShow | 查看人设 | Name: 组名称, AgentName: Agent名 |
| POST | /api/agentsingle_single/RoleSave | 保存人设 | Name: 组名称, AgentName: Agent名, Content: 人设内容 |
| POST | /api/agentsingle_single/MemoryShow | 查看记忆 | Name: 组名称, AgentName: Agent名 |
| POST | /api/agentsingle_single/MemorySave | 保存记忆 | Name: 组名称, AgentName: Agent名, Content: 记忆内容 |
| POST | /api/agentsingle_single/MemoryedShow | 查看上次概括前记忆 | Name: 组名称, AgentName: Agent名 |
| GET | /api/agentsingle_single/MemoryAgent | 调用记忆概括Agent | WebSocket, URL参数: group, agent |
| GET | /api/agentsingle_single/ToolTools | 添加/修改工具 | WebSocket, URL参数: group, agent, action(c/m), tool |
| POST | /api/agentsingle_single/AgentToolsDelete | 删除工具 | Name: 组名称, AgentName: Agent名, action: "d", tool: 工具名 |
| GET | /api/agentsingle_single/ToolsList | 列出暂存区工具 | 无 |
| POST | /api/agentsingle_single/AgentToolsList | 列出Agent已安装工具 | Name: 组名称, AgentName: Agent名 |
| GET | /api/agentsingle_single/AgentCorresspond | Agent总通信模块 | WebSocket, URL参数: group |


### WebSocket 通信协议

记忆概括 Agent：
  连接: ws://host/api/agentsingle_single/MemoryAgent?group=xxx&agent=xxx
  前端发送: 纯文本消息
  后端返回: Python print 实时输出

工具操作 Agent：
  连接: ws://host/api/agentsingle_single/ToolTools?group=xxx&agent=xxx&action=c/m&tool=xxx
  action: c=添加, m=修改
  前端发送: 纯文本消息
  后端返回: Python print 实时输出

Agent 通信模块：
  连接: ws://host/api/agentsingle_single/AgentCorresspond?group=xxx
  前端发送 JSON:
    {
      "agent": "all" 或 "agent名",
      "caller": "user",
      "out_input": "消息内容"
    }
  后端返回: Python print 实时输出


### Go 与 Python 进程通信方式

| 场景 | 方式 | 说明 |
|------|------|------|
| 一次性操作 | exec.Command + CombinedOutput | 创建/删除/改名，等Python跑完拿结果 |
| 持续对话 | exec.Command + stdin/stdout管道 | Agent运行、工具操作、记忆概括 |
| 前端实时推送 | goroutine读stdout → WebSocket → 前端 | Python每print一次，前端立刻显示 |


### 全局进程管理

| 函数 | 作用 |
|------|------|
| startPython(group, agent) | 启动Agent主程序，返回管道 |
| startPython2(group, agent, action, tool) | 启动工具操作，返回管道 |
| startPython3(group) | 启动通信模块，返回管道 |


## 实现清单

| 设计 | 实现 |
|------|------|
| 文件系统隔离 | agents/组/agent/ 结构 |
| 注册表 | agents_login.json |
| 创建/删除 Agent | generate.py / Go 直接操作 |
| 工具注册 | desmake.py 管道调用 |
| 人设/记忆管理 | HTTP API + Web 编辑 |
| 记忆概括 | WebSocket + Python 管道 |
| 通信机制 | WebSocket + JSON 协议 |
| 暂存区 | staging/ + 前端管理 |
| 模板复制 | agent_frame/ → 新 Agent |
| 并发管理 | goroutine + sync.Mutex |
| Go 启停 Python | exec.Command + stdin/stdout |


## 技术栈

- 后端：Go（net/http、gorilla/websocket、os/exec、bufio）
- Agent：Python（sys.stdin/stdout 管道通信、shutil、pathlib）
- 前端：原生 HTML/CSS/JavaScript（fetch、WebSocket、File API）
- 通信：HTTP API + WebSocket + stdin/stdout 管道
- 存储：文件系统（JSON + TXT）
- 并发：goroutine + sync.Mutex + channel




