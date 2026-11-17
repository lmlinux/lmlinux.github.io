# lmlinux.github.io

AI 相关的技术分享与知识库：<https://lmlinux.github.io>

MkDocs + Material 主题，GitHub Pages 托管，push 到 `main` 自动构建部署。

## 本地预览

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve     # http://localhost:8000
```

## 写一页内容

在 `docs/ai/` 下新建 Markdown，并在 `mkdocs.yml` 的 `nav` 里挂上：

```yaml
---
comments: true   # 可选：开启 giscus 评论区
---
# 标题
正文……
```

## 结构

- `docs/ai/` — Artificial Intelligence
- `hooks.py` — giscus 评论注入
- `mkdocs.yml` — 导航 / 主题 / 插件配置
- `.github/workflows/deploy.yml` — 部署流水线
