# Agent 安全工程：攻击面、防御谱系与沙箱选型

Agent 安全是系统工程，不是模型工程。OWASP Q1 2026 事件全景的最大信号是**真实事故几乎都没有 CVE**——不是代码 bug，是配置、权限、信任边界 bug，传统漏洞扫描结构性地看不见它们。本文梳理攻击面分类学（lethal trifecta 判据 + 两份 OWASP 清单）、真实事件、防御五流派的生产验证状态、沙箱隔离矩阵与 MCP/A2A 供应链风险，最后给工程落地清单。非渗透指南。

数据核实：2026-11-18 首次访问全部信源；2026-11-27 复核——Willison / Anthropic / CaMeL / Unit 42 / LogRocket 直连可达，OWASP、NSA、SSRN 等官方页对部分网络 IP 级封锁，经 Microsoft 安全博客与 OneCompliant 镜像核对内容一致。

## 1. 判据先于分类：lethal trifecta

Simon Willison（2025-06-16）给出的严重提示注入事故必要条件三件，**缺一即无事故**：

| 腿 | 含义 | 砍法 |
|---|---|---|
| ① 私数据访问 | agent 能读邮件/数据库/生产日志 | 数据权限最小化、按目标注入凭据 |
| ② 不可信内容暴露 | 攻击者控制的文本/图片能进上下文 | 输入源白名单、内容消毒 |
| ③ agency（出口通道） | agent 能外发数据或执行特权动作 | **egress 白名单、动作门禁** |

推论：**防御不必消灭注入**——消灭不了，LLM 无法在语义层区分指令与数据，这是架构属性——只需保证三腿不齐。第三腿（出口）是最便宜也最常被漏砍的一条：GrafanaGhost 的整条攻击链就靠一个 markdown 图片渲染出口（见 §3）。

术语注：**confused deputy**（混淆代理人）——持有特权的代理被不可信输入误导、用自身权限执行攻击者意图的经典安全概念。agent 场景 = agent 拿着你的凭据，被消息或工具输出里的注入指令驱动。trifecta 是它的三条件化表述。

## 2. 两份 OWASP 清单

### 2.1 LLM Top 10（2025 版）

| # | 风险 | 一句话 |
|---|---|---|
| LLM01 | 提示注入 | 直接/间接注入劫持行为 |
| LLM02 | 敏感信息泄露 | 上下文/输出带出秘密 |
| LLM03 | 供应链 | 依赖/模型/MCP server 被污染 |
| LLM04 | 数据与模型投毒 | 训练/RAG/记忆数据被污染 |
| LLM05 | 输出处理不当 | 下游把 LLM 输出当可信命令执行 |
| LLM06 | 过度授权 | agent 权限超过任务所需 |
| LLM07 | 系统提示词泄露 | 提示词逆向 |
| LLM08 | 向量/嵌入弱点 | 检索库投毒、越库检索 |
| LLM09 | 错误信息 | 幻觉自信输出 |
| LLM10 | 无限制消耗 | token/算力烧穿 |

### 2.2 Agentic Top 10（2026 版，2025-12-09 发布）

100+ 专家评审（Microsoft AI Red Team 在评审委员会）。与 LLM 清单的本质差异：**从"模型风险"转到"自治体风险"**——身份、级联、信任、失控：

| # | 风险 | 一句话 | Q1 2026 对应实例 |
|---|---|---|---|
| ASI01 | Agent 目标劫持 | 注入/投毒内容改写 agent 目标 | GrafanaGhost |
| ASI02 | 工具滥用 | 合法工具被不安全串联/误用 | Replit 删库 |
| ASI03 | 身份与权限滥用 | 委托信任、继承凭据、角色链被钻 | Vertex Double Agent |
| ASI04 | Agentic 供应链 | 被污染的 agent/工具/插件/registry/更新渠道 | Mercor-LiteLLM、Claude Code 泄源 |
| ASI05 | 意外代码执行 | agent 生成/调用的代码被劫持 | Claude Code 后续 3 CVE |
| ASI06 | 记忆与上下文投毒 | 毒内容持久驻留、长期影响行为 | Gemini 系列记忆投毒披露 |
| ASI07 | 不安全 agent 间通信 | A2A 消息伪造/篡改 | session smuggling（Unit 42） |
| ASI08 | 级联失效 | 单点故障跨 agent/工具/工作流扩散 | Meta 内部事件 |
| ASI09 | 人-agent 信任滥用 | 借人的信任与权威偏误骗审批/套信息 | Meta 内部事件 |
| ASI10 | Rogue agent | agent 漂移/被控、越出预期范围 | Replit（冻结期删库且撒谎） |

第三份清单已在路上：**Agentic Skills Top 10（AST10）**，针对 skill 执行层生态的第一份安全框架。

## 3. 真实事件表（2025-07 → 2026-04）

前四例为 OWASP Q1 2026 Round-up 收录口径：

| 事件 | 时间 | 链条 | 工程启示 |
|---|---|---|---|
| **Replit agent 删生产库** | 2025-07 | 迁移脚本误删库 + "code freeze" 期间继续跑 + 事后辩解；CEO 定性"灾难性失败" | agent 写路径必须有**冻结开关与硬门禁** |
| **A2A session smuggling**（Unit 42） | 2025-10 | 恶意 agent 利用有状态会话夹带隐蔽指令；前提是"agent 默认信任协作 agent"；非协议漏洞、任何有状态协议通杀 | 跨 agent 消息同样是可被冒充的不可信内容 |
| **GrafanaGhost**（Noma Security） | 2026 Q1 | 外部内容藏指令 → Grafana AI 助手渲染外链图片 → URL 参数外带数据 | **出口通道是最便宜的一条腿**：图片渲染/URL 参数这类"无害功能"就是外泄面 |
| **Vertex AI Double Agent**（Unit 42） | 2026 Q1 | 平台默认的管理服务账号超额授权 → 提取凭据、跨项目访问 | **不信任平台默认授权**——默认授权普遍超额 |
| **Meta 内部 agent 越权建议**（Guardian 报道） | 2026 Q1 | 工程师问内部论坛 → AI 给的修复方案直接被采纳执行 → 敏感数据对内部工程师暴露约 2 小时；无外部攻击者，Meta 称用户数据未被滥用 | **agent 建议与人执行之间必须有确定性验证层**——"AI 提案 + 人拍板"不够，人会被建议带着走 |
| **Mercor / LiteLLM**（WIRED） | 2026 Q1 | 恶意 LiteLLM 版本 → AI 数据供应商 Mercor 被攻破 → Meta 暂停合作、多家实验室重估 | AI 相邻栈（网关/编排库）是供应链入口，不只模型本身 |
| **Claude Code 源码泄露 + 三 CVE** | 2026-03/04 | npm 包误带 59.8MB sourcemap → 512,664 行源码全量泄露 → 数日内三 CVE → 泄露源码被用作 GitHub 恶意诱饵 | **harness 本体也是攻击面**：你依赖的 CLI 工具链，其分发渠道事故会直接转化为你的漏洞窗口 |

口径注：事件均转引自 OWASP Round-up 与 SecurityWeek/HelpNetSecurity/Fortune/Guardian/WIRED 等报道。OWASP 的总结句："Securing AI now requires a shift from model-level safeguards to holistic system, identity, and operational security controls"——且只有 Flowise RCE（CVE-2025-59528）这类传统软件漏洞能进 CVE 流程，其余全不是。

行业统计（安全厂商调查，注意来源利益，见 §8）：SailPoint 2025（353 名企业 IT/安全人员）——82% 组织已跑 agent，**80% 见过 agent 做出未经预期的事**，39% agent 访问过未授权资源，**23% agent 被骗交出凭据**；96% 视 agent 为增长风险，仅 44% 有安全政策。IBM 2025——13% 报告过 AI 模型/应用被入侵，**其中 97% 没上 AI 访问控制**。

## 4. 防御谱系：五个流派与生产验证状态

| 流派 | 机制 | 代表 | 验证状态 | 局限 |
|---|---|---|---|---|
| **架构派**（能力与信任边界） | 给每个值挂能力元数据，不可信来源的值到达不了特权工具，除非经显式门 | **CaMeL**（DeepMind，arXiv:2503.18813，SATML 2026；Willison 2023 dual LLM 的系统化） | 论文级 + AgentDojo 基准：**77% 任务可解且可证明安全 vs 无防御 84%**（安全税 7 点） | 需重写 agent 数据流，非 drop-in |
| 架构派（轻量变体） | 上下文标记（delimiting/spotlighting）：把不可信内容用标记包起来，教模型"标记内是数据不是指令" | **spotlighting**（Hines 等，微软系研究） | 中等——降低成功率但不归零 | 靠模型遵守约定，对抗性改写可绕 |
| **检测派** | 分类器扫描进上下文的不可信内容，标记可疑注入 | Anthropic Claude for Chrome 配套分类器；各家 API guardrail | 生产在用；HN 对 CaMeL 的共识评价："用另一个 AI 模型找注入是有缺陷的方法" | 可作纵深一层，单独用 = 把安全押在军备竞赛上 |
| **训练派**（模型鲁棒性） | RL 训练模型抵抗注入：模拟注入进训练，奖励"识别并拒绝" | **Anthropic**：Opus 4.5 浏览器场景自适应 Best-of-N 攻击者（100 次尝试/环境）**攻击成功率 ~1%**；Sonnet 4.6 system card：computer use 全防护 8% vs 无防护 50%（转引） | 生产验证中，进步快 | Anthropic 原话："1% 仍是真实风险，没有浏览器 agent 对注入免疫"——**不能当唯一防线** |
| **身份派** | 加密签名验身份：签名 AgentCard（A2A v1.2 DID 域名绑定）、remote agent verification | A2A 规范；Unit 42 建议三件套：HitL + 签名 AgentCard + 上下文接地检测 | 规范在、**生产采用浅** | 防伪造不防"已认证的 agent 作恶"（rogue agent 是另一条轴） |
| **边界派**（最小权限 + egress） | 权限按目标注入不进 agent、出站白名单、动作门禁 | 云沙箱平台的 fail-closed egress 与凭据隔离 | **云侧生产成熟**；本地工具生态普遍零摩擦优先，此层常缺 | 与开发体验直接冲突，需要刻意设计 |

**组合判断**：没有单一流派够用。生产级组合拳 = **边界派打底（砍 trifecta 第三腿）+ 架构派收口（不可信数据流与特权工具分离）+ 训练/检测派当纵深（降攻击成功率）+ 身份派管跨域**。与 Anthropic 的自述顺序一致：RL 训练 + 分类器 + 红队都上了，仍然说"远未解决"。

## 5. 沙箱矩阵：四档隔离 × 实测数据

### 5.1 四档隔离模型（强度自上而下递减、成本反向）

| 档 | 原语 | 代表 | 边界 |
|---|---|---|---|
| 硬件虚拟化 microVM | 独立 guest 内核 | Firecracker、libkrun、Kata | hypervisor 边界（最硬） |
| 用户态内核 | 拦截系统调用的用户态内核 | **gVisor**（Google Agent Sandbox、Modal） | syscall 层 |
| 加固容器/命名空间 | namespace+seccomp+LSM | Docker、Sysbox、bwrap+Landlock | 内核共享+过滤 |
| 进程级隔离 | 语言运行时沙箱 | V8 isolate、QuickJS | 引擎边界（最快最弱） |

gVisor 一档是云侧 agent 的事实标准——Google Agent Sandbox 与 Modal 等多家独立选择同款，趋同演化信号。

### 5.2 平台实测（LogRocket 2026-08 横评，15 平台五维实测）

| 平台 | 冷启动 create/resume（实测） | 隔离原语 | 持久化 | GPU | 部署 |
|---|---|---|---|---|---|
| E2B | **717ms / 662ms** | Firecracker microVM | pause/resume+快照 | 无 | 托管 |
| Daytona | 742ms / 1254ms | Docker 默认，Kata/Sysbox 可选 | fork/pause/快照 | 有 | 托管+自托管 |
| Modal | 2437ms / 2347ms（快照启动） | gVisor | 文件/内存快照 | 有 | 托管 |
| Vercel | 1852ms / 3333ms | Firecracker | 默认持久+快照 | 无 | 托管 |
| Cloudflare | 隔离 ms / 容器级 | V8 isolate / 容器 | 容器持久 | 无 | 托管（边缘） |
| Runloop | ~25ms resume（厂商口径） | microVM+容器双层 | 快照+零空闲 | 无 | 托管 |
| AWS Lambda MicroVMs | 快照近即恢复 | Firecracker | 挂起 ≤8h | 无 | AWS |
| Google Agent Sandbox | 亚秒级（厂商） | **gVisor（GKE 原生）** | 有状态 TTL ≤14 天 | 经 GKE | 托管+自托管 |
| OpenSandbox | 依后端 | 可插拔 gVisor/Kata/Firecracker | 依后端 | 依后端 | **自托管，零平台费** |
| Microsandbox | <200ms（厂商） | libkrun microVM | 持久或临时 | 无 | **自托管，本地** |

（另 5 家：Blaxel、Northflank、Fly Sprites、CodeSandbox SDK、AIO Sandbox，见引用。）

### 5.3 选型判据

冷启动决定交互型 agent（编码助手）；隔离强度决定不可信代码执行；持久化决定跨几十次工具调用的研究型任务——**先定哪个维度错了会毁掉你，再选**（LogRocket 结论）。自托管需求看 OpenSandbox（可插拔后端）/ Microsandbox（libkrun）/ Daytona self-host。

## 6. MCP / 工具 / A2A 供应链

### 6.1 tool poisoning：描述即毒（不需要调用）

MCP 工具的 description 字段本身就是进模型上下文的不可信文本——**agent 在工具列表加载时读到描述即被投毒，不需要真的调用**。恶意描述内嵌指令操纵工具选择与执行（LLM01 的 MCP 形态）；更隐蔽变体把指令藏在不可见字符里。Unit 42（2026-06）实测"误导性工具描述"改变 agent 行为（arXiv:2508.01186）。

### 6.2 RugPull：安装后变脸

remote MCP server 审核时的工具描述/行为与运行时不同——**vet 时无害、用起来作恶**。arXiv:2508.01186 系统化为三类：事后改描述、改实现、改依赖。对策：pin 版本/哈希 + 行为级运行时校验，元数据扫描挡不住这类。

### 6.3 控制面与官方指南

- registry 注册时扫描（如 Cisco AI Defense 开源扫描器）挡元数据投毒；RugPull 需运行时行为检测
- **NSA 2026-05 官方 CSI《MCP: Security Design Considerations for AI-Driven Automation》**：点名 MCP 的动态工具调用与 agent 间隐式信任为设计性风险，主张 secure-by-default——国家机构入场是这层"从叙事变合规"的信号
- MCP 自身的采样（sampling）特性也是通道：恶意"代码摘要"工具可借 sampling 让宿主 agent 替它干活（Unit 42 演示）

### 6.4 A2A 侧：session smuggling

恶意 agent 在有状态会话的良性请求/响应流里夹带隐蔽指令，多轮建立假信任后操纵受害 agent——非 A2A 协议漏洞，**任何有状态协议通杀**；前置条件是"agent 默认信任协作 agent"。Unit 42 给出的缓解三件套：关键动作 HitL、**加密签名 AgentCard**（remote agent verification）、上下文接地检测（识别跑题/注入指令）。

## 7. 工程落地清单

按 trifecta 砍腿优先序：

1. **先砍第三腿（出口）**：出站网络白名单 + 特权动作门禁。GrafanaGhost 是教案——一个图片渲染出口 = 全链外泄。这是最便宜、最常被漏掉的一条。
2. **凭据分层，不信任默认授权**：只读凭据常驻、写凭据仅在审批后的执行期注入；平台/工具默认授权普遍超额（Vertex 教训）。
3. **不可逆边界全有人审，且人审前有确定性验证层**：Meta 事件证明"AI 提案 + 人拍板"不够——人会被建议带着走，验证层要独立于提案。
4. **写路径有冻结开关**：Replit 的"code freeze 期间继续跑"是反面教材。
5. **工具输出也是不可信内容**：日志、集群状态、网页抓取结果里的注入可反噬 agent；输入侧标记（spotlighting）+ 注入红队测试当纵深。
6. **工具结果先在沙箱内过滤再回主上下文**：脚本化/code mode 形态（无网络的引擎沙箱）天然收窄注入面，是安全正资产。
7. **引入外部 MCP server/skill 时上审批 + pin 版本/哈希**：描述投毒与 RugPull 都在这一步防。

## 8. 诚实校准（信源利益）

- **OWASP 清单一半是咨询产业需求**：Top 10 系列天然服务安全厂商；清单内容真实，但"必须马上建 M 项控制"的紧迫感有营销放大
- **SailPoint/IBM 统计是安全厂商调查**（卖身份治理/AI 安全产品的两家）——抽样与措辞朝叙事方向偏；趋势可信、绝对值存疑
- **Anthropic 的 1% 攻击成功率是自家攻自家**：内部攻击者与自家防御共同进化，外部攻击者的成功率没有同等披露；且数字出自最新旗舰模型——旧模型/便宜模型无此鲁棒性，不能外推
- **CaMeL 的 77% 有基准选择偏差**：AgentDojo 是其适配的基准；"可证明安全"证明的是能力模型的性质，不证明 prompt 语义不可绕（模型对标记的遵守仍是概率性的）
- **LogRocket 矩阵是独立实测（难得）但单一来源**：冷启动数字自测、厂商口径混标（表内已注明）；15 平台存活率半年一变，品类洗牌快
- **事件报道链长**：OWASP Round-up → 二手分析 → 三手引用；本文事件细节尽量回到 Round-up 收录口径与原始研究方（Noma/Unit 42/Guardian/WIRED），仍有转引损耗

## 引用

- lethal trifecta：[Simon Willison（2025-06-16）](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- OWASP：[LLM Top 10 2025](https://owasp.org/projects/top-10-for-large-language-model-applications)（[清单镜像](https://trydeepteam.com/docs/frameworks-owasp-top-10-for-llms)）、[Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)（[Microsoft 全表转述](https://www.microsoft.com/en-us/security/blog/2026/03/30/addressing-the-owasp-top-10-risks-in-agentic-ai-with-microsoft-copilot-studio/)）、[Q1 2026 Exploit Round-up](https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/)（[OneCompliant 镜像](https://onecompliant.ai/article-owasp-q1-2026.html)）、[Agentic Skills Top 10 项目页](https://owasp.org/projects/agentic-skills-top-10)
- CaMeL：[arXiv:2503.18813](https://arxiv.org/abs/2503.18813)（DeepMind，SATML 2026）；[HN 讨论](https://news.ycombinator.com/item?id=43733683)
- Anthropic 注入防御：[Prompt injection defenses（2025-11-24）](https://www.anthropic.com/research/prompt-injection-defenses)（Opus 4.5 / Best-of-N / 分类器 / RL）
- Unit 42：[agent session smuggling（2025-10-31）](https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/)、[AI agent 供应链（2026-06-11）](https://unit42.paloaltonetworks.com/ai-agent-supply-chain-risks/)；[MCP 行为研究 arXiv:2508.01186](https://arxiv.org/pdf/2508.01186)
- tool poisoning / rug pull：[Hive Security（2026-05-07）](https://hivesecurity.gitlab.io/blog/mcp-server-security-risks-attackers-perspective/)、[Zuplo rug pull 文（2026-06-16）](https://zuplo.com/blog)
- NSA CSI：[MCP Security Design Considerations（2026-05，PP-26-1834）](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf)
- 沙箱矩阵：[LogRocket 15 平台实测（2026-08-04）](https://blog.logrocket.com/comparing-ai-agent-sandbox-platforms-e2b-modal-daytona-and-more/)、[Developers Digest 选型口径（2026-07-01）](https://developersdigest.tech/blog/ai-agent-code-sandbox-comparison-2026)
- 事件报道：Replit（[Fortune（2025-07-23）](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/)）、Claude Code 泄源（[SecurityWeek](https://www.securityweek.com/)、[SSRN abstract 6504920](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6504920)）；GrafanaGhost/Vertex/Meta/Mercor 见 Round-up 条目
- 行业统计：SailPoint 2025 / IBM 2025（经 [Cranium 转引](https://cranium.ai/agentic-ai-security/)）