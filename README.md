# lmlinux.github.io

Source for <https://lmlinux.github.io>, built with MkDocs Material and deployed to GitHub Pages.

The site contains bilingual lmlinux landing and download pages, links to the canonical project documentation, and Artificial Intelligence technical notes:

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

- `docs/index.md` — Chinese product landing page
- `docs/lmlinux/` — Chinese lmlinux overview and download page
- `docs/en/` — English landing, overview, and download pages
- `docs/ai/` — Artificial Intelligence notes
- `hooks.py` — giscus comment integration
- `mkdocs.yml` — navigation, theme, and plugin configuration
- `.github/workflows/deploy.yml` — deployment workflow
