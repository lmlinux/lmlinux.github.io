# lmlinux.github.io

Source for <https://lmlinux.github.io>, built with MkDocs Material and deployed to GitHub Pages.

The homepage is a directory for the lmlinux project and personal Artificial Intelligence notes. Separate, cross-linked Chinese and English lmlinux pages provide overview and download summaries and link to canonical project documentation:

- Chinese project page: <https://lmlinux.github.io/lmlinux/>
- English project page: <https://lmlinux.github.io/en/lmlinux/>
- Technical notes: <https://lmlinux.github.io/ai/>

## Local preview

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve -a 127.0.0.1:8001
```

Open <http://127.0.0.1:8001/>. Port **8001** is the local preview port for this repository.

## Build

```bash
.venv/bin/mkdocs build --strict
```

## Structure

- `docs/index.md` — Chinese project and personal-notes directory
- `docs/lmlinux/` — Chinese lmlinux overview and download page
- `docs/en/` — English directory and lmlinux overview/download pages
- `docs/ai/` — Artificial Intelligence notes
- `hooks.py` — giscus comment integration
- `mkdocs.yml` — navigation, theme, and plugin configuration
- `.github/workflows/deploy.yml` — deployment workflow
