from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 配置真实的上游模型名、服务地址和凭证；缺少必填项时会在启动阶段报错。
    chat_model: str
    # 三组上游各自直连,不经网关。base_url 和 key 跟着账号走,所以和 chat_model 一样必填;
    # 嵌入和重排都在硅基流动、地址固定,给了默认值,只有 key 要填。
    chat_base_url: str
    chat_api_key: str
    embed_base_url: str = "https://api.siliconflow.cn/v1"
    embed_api_key: str
    rerank_base_url: str = "https://api.siliconflow.cn/v1"
    rerank_api_key: str
    # 可选的推理链参数，是否生效由聊天模型服务决定。
    chat_thinking: str = ""           # disabled 关 / adaptive 开
    chat_reasoning_effort: str = ""   # 开着时的强度:low / high / max
    chat_reasoning_split: str = ""    # MiniMax 专属:true 让思考进 reasoning_content 独立字段,
                                      # 而不是混在 content 里的 <think>。关不掉思考链时靠它兜底
    token_budget: int = 2000
    database_url: str = "mysql+asyncmy://root:root@localhost:3306/evanhelp"
    test_database_url: str = "mysql+asyncmy://root:root@localhost:3306/evanhelp_core_test"
    # 知识检索
    embed_model: str = "BAAI/bge-m3"          # 上游真实名(无网关别名可用)
    milvus_uri: str = "http://localhost:19530"   # retrieval: Lite → Standalone
    # 混合检索与重排
    rerank_model: str = "BAAI/bge-reranker-v2-m3"   # 上游真实名
    recall_top_k: int = 50        # dense/BM25 各召回 Top-50
    rerank_top_k: int = 10        # 精排出 Top-10
    subquery_split: bool = True   # 一问多意图时按子句拆开各检索一遍再轮转合并(见 retrieval)
    rerank_min_score: float = 0.3 # 重排最高分低于此 → 检索证据低,拒答
    # 工作流编排
    max_agent_steps: int = 6              # ReAct 环最大步数(封顶,超则兜底)
    # Agent 循环按步数限制；token 用量记录到 trace，但不作为停止条件。
    checkpointer_db_path: str = "data/conversation_checkpoints.sqlite"  # LangGraph checkpointer(data/*.db* 已 gitignore)
    # 意图识别模型配置
    intent_model: str = ""            # 意图识别模型名;空=回落 chat_model
    intent_small_model: str = ""      # 降级路小模型(种子,未接运行时)
    intent_mode: str = "accuracy"     # accuracy=只用大模型;cost=小模型判→低置信升级大模型(未实现)
    intent_conf_threshold: float = 0.6  # cost 模式升级阈值(种子)
    # 会话上下文管理
    summary_trigger_messages: int = 30    # 距上次摘要新增满多少条触发后台任务
    context_window_turns: int = 8         # 摘要后保留原文的最近轮数(需求 5-10 取中)
    context_window_max_tokens: int = 3000 # 滑窗 token 上限(trim_messages 兜底)
    summary_model: str = ""               # 摘要模型,空=回落 chat_model
    # 工具注册、执行与 MCP 接入
    mcp_logistics_url: str = "http://127.0.0.1:8101/mcp"    # 物流 MCP Server
    mcp_aftersales_url: str = "http://127.0.0.1:8102/mcp"   # 售后 MCP Server
    tool_default_timeout: float = 5.0    # 内置工具默认超时(秒)
    mcp_tool_timeout: float = 10.0       # MCP 工具默认超时(走 HTTP,放宽)
    tool_max_retries: int = 2            # 只读工具暂时性故障最大重试次数
    demo_ticket_delay_seconds: float = 0.0  # 验收 6:>0 时 create_ticket 人为变慢(写超时演示)
    # 可选的 Langfuse 调用追踪；未配置时应用仍可正常启动
    # Langfuse 服务配置
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_base_url: str = ""     # 如 http://localhost:3000(自部署地址,数据不出门)
    # observability 置信度闸(正式版):阈值由 make calibrate-confidence 在 retrieval 评估集上校准回填,不拍脑袋
    # 实测:可答桶 p50=0.715 vs 应拒桶 p50=0.105/max=0.251,YoudenJ 最优点 0.26
    # (可答通过率 85%、应拒放行率 0%,报告见 data/observability/reports/confidence_calibration.txt,
    #  「观测与成本」页 /observability 上也能看,推荐值与这里不一致时页面会标出来)
    evidence_confidence_threshold: float = 0.26


settings = Settings()
