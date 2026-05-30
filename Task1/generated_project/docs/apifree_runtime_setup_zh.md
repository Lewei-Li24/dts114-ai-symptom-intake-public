# APIFree API 选择与运行配置

本项目使用 APIFree 作为 OpenAI-compatible 大模型入口。API key 不写入代码、不放进 GitHub、不放进截图，只在运行 Flask 时通过环境变量输入。

前端页面不直接调用 APIFree。正确链路是：前端按钮调用本项目 Flask `/api/...` 接口，Flask 再带 `Authorization: Bearer APIFREE_API_KEY` 调用 APIFree，最后 Flask 把 JSON 返回给前端。这样 API key 不会暴露在浏览器里。

## 推荐 API

| 功能 | 选用 API | 项目位置 |
| --- | --- | --- |
| 症状追问、摘要、护理建议、体检单结构化、UML 生成 | `POST https://api.apifree.ai/v1/chat/completions` | 后端 `app.py` 的 `call_model_json()` |
| 查看 key 可用模型 | `GET https://api.apifree.ai/v1/models` | 后端 `/api/ai/models` |
| 测试模型是否能返回 JSON | `POST /api/ai/test` | 本项目诊断接口 |

## 推荐模型

```text
deepseek-ai/deepseek-v4-flash
```

该模型适合课程演示中的普通文本生成、追问、摘要、结构化 JSON 和 PlantUML 生成。最终演示如果需要更强输出，可在 APIFree 控制台确认后切换到可用的更强模型。

## 环境变量

```powershell
$env:APIFREE_API_KEY="你的 APIFree key"
$env:APIFREE_BASE_URL="https://api.apifree.ai/v1"
$env:APIFREE_MODEL="deepseek-ai/deepseek-v4-flash"
python app.py
```

也可以复制 `.env.example` 为 `.env` 做本地演示，但 `.env` 已被 `.gitignore` 排除，不能提交到 GitHub。

## 会调用 APIFree 的本项目接口

- `/api/intake-chat`：对话式症状采集。
- `/api/sessions/<id>/followup`：按 session 生成追问。
- `/api/sessions/<id>/summary`：生成结构化症状摘要。
- `/api/sessions/<id>/care-guidance`：生成护理建议、药物讨论参考表、解决方案计划表。
- `/api/health-records/analyze`：结构化体检单文字。
- `/api/profiles/<id>/checkup-structure`：按用户档案结构化体检信息。
- `/api/uml/generate`：根据业务问题生成 PlantUML。

地图、浏览器定位、图片识别和报告图片生成功能已经从最终版本移除。当前版本保留 APIFree 文本生成链路：追问、摘要、护理建议、体检单文字结构化和 UML 生成。

## GitHub 提交注意

不要提交：

- `.env`
- API key
- 真实患者信息
- 真实体检报告

可以提交：

- `app.py`
- `templates/`
- `static/`
- `docs/`
- `tests/`
- `requirements.txt`
- `Dockerfile`
- `.github/workflows/ci.yml`

## 官方参考

- APIFree docs: https://docs.apifree.ai/
- PlantUML: https://plantuml.com/
