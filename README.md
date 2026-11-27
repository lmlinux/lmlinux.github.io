# lmlinux.github.io

Source for <https://lmlinux.github.io>, built with MkDocs Material and deployed to GitHub Pages.

The homepage presents two linked entries as cards, one per row: lmlinux and Artificial Intelligence. A single lmlinux page provides equivalent Chinese and English overview/download summaries through clickable language tabs and links to canonical project documentation:

- Bilingual project page: <https://lmlinux.github.io/lmlinux/>
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

- `docs/index.md` — two-entry Chinese homepage (card grid)
- `docs/stylesheets/extra.css` — homepage card layout overrides
- `docs/lmlinux/` — single bilingual lmlinux page with clickable language tabs
- `docs/ai/` — Artificial Intelligence notes
- `hooks.py` — giscus comment integration
- `mkdocs.yml` — navigation, theme, and plugin configuration
- `.github/workflows/deploy.yml` — deployment workflow
