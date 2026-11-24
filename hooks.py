"""MkDocs hooks：给 front matter 里声明 `comments: true` 的页面追加 giscus 评论区。

giscus 数据存放于本仓库的 GitHub Discussions，访客用 GitHub 账号评论。
"""

_GISCUS = """
<div class="giscus-comments" style="margin-top: 2.5rem; border-top: 1px solid rgba(128,128,128,.25); padding-top: 1.5rem;">
  <script
    src="https://giscus.app/client.js"
    data-repo="lmlinux/lmlinux.github.io"
    data-repo-id="R_kgDOOBFI4w"
    data-category="Announcements"
    data-category-id="DIC_kwDOOBFI484DLQmX"
    data-mapping="pathname"
    data-strict="0"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="top"
    data-theme="preferred_color_scheme"
    data-lang="zh-CN"
    data-loading="lazy"
    crossorigin="anonymous"
    async></script>
</div>
"""


def on_page_content(html, *, page, config, files):
    if page.meta.get("comments"):
        return html + _GISCUS
    return html
