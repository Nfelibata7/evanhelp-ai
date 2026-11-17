# 本地部署

本文说明如何在本机启动 EvanHelp。首次运行需要 Python 3.12+、uv、Docker Compose、GNU Make 和 Bash；Windows 推荐在 WSL2 中运行 Makefile 命令。

## 1. 安装依赖并配置模型

```bash
uv sync
cp .env.example .env
```

在 `.env` 中配置聊天、Embedding 和 Rerank 服务。至少填写 `CHAT_BASE_URL`、`CHAT_MODEL`、`CHAT_API_KEY`、`EMBED_API_KEY` 和 `RERANK_API_KEY`。配置模板中的密钥只是占位值，不能直接用于请求。

## 2. 启动存储服务并准备样例资料

```bash
docker compose up -d
make seed
make kb-build
make kb-vectorize
```

Compose 启动 MySQL、Milvus 及其依赖。`make seed` 导入 FAQ 演示数据；`make kb-build` 将 `data/kb/` 中的 Markdown 资料切块写入 MySQL；`make kb-vectorize` 调用 Embedding 服务并写入 Milvus。

## 3. 启动应用

```bash
make dev
```

该命令启动两个 MCP 服务和 FastAPI 应用。访问：

- 客服页面：<http://localhost:8000>
- API 文档：<http://localhost:8000/docs>
- 知识管理：<http://localhost:8000/kb>
- 运营复核：<http://localhost:8000/review>

可在聊天页面输入“订单 1001 的物流到哪了”，查看 Agent 调用订单与物流工具的过程。样例订单和业务 MCP 服务返回的是本地模拟数据。

## 常用命令

```bash
make help           # 查看全部 Make 目标
make test           # 运行不调用外部模型的测试
make seed-conv      # 加载用于离线处理的样例会话
make dev-down       # 停止应用与 MCP 服务
docker compose down # 停止 MySQL、Milvus 等容器
```

分类器训练和 Langfuse 自托管为可选组件，需要额外依赖或配置。请先查看对应 Make 目标和 Compose 文件，再按需启动。不要将真实密钥写入仓库。