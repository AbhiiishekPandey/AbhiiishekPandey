# Setup & regeneration notes

This repo renders `README.md`, which GitHub shows on your profile page at
github.com/AbhiiishekPandey. The three images it embeds are pre-rendered
animated SVGs, not live services — nothing calls out to third-party stat
widgets.

## First-time setup (already done for you)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

## Files

| File | What it is | How it's kept fresh |
|---|---|---|
| `avi-ascii.svg` | Self-typing ASCII portrait | Regenerate manually when you change your photo |
| `info-card.svg` | Neofetch-style panel | Regenerate manually when you update your bio |
| `contrib-heatmap.svg` | Real contribution calendar | Auto-refreshed daily by GitHub Actions |
| `data/contributions.json` | Raw scraped data behind the heatmap | Auto-refreshed daily |

## Regenerating the portrait (only if you swap the photo)

```bash
python scripts/prep_photo.py your-new-photo.jpg
python scripts/make_ascii_svg.py
```

`prep_photo.py` removes the background (rembg), boosts local contrast
(OpenCV CLAHE), and composites onto white so the background maps to blank
space in the ASCII ramp. The first run downloads a ~176MB background-removal
model — that's normal and only happens once.

## Regenerating the info card (when your bio/stack changes)

Edit the `FIELDS` list at the top of `scripts/make_info_card.py`, then:

```bash
python scripts/make_info_card.py
```

Set `STATIC=1` before the command to emit a frozen (non-animated) frame,
useful for a quick local preview since most image viewers don't play SMIL.

## Regenerating the heatmap manually

```bash
python scripts/fetch_contributions.py AbhiiishekPandey
python scripts/render_heatmap_svg.py
```

This scrapes `https://github.com/users/AbhiiishekPandey/contributions` — the
same public HTML fragment your profile page uses — so no API token is
required. It's already wired into `.github/workflows/update-profile-art.yml`
on a daily cron (`17 6 * * *` UTC) plus `workflow_dispatch` for manual runs.

## Publishing

```bash
git init
git add .
git commit -m "profile readme: animated ASCII + neofetch card + live heatmap"
git branch -M main
git remote add origin https://github.com/AbhiiishekPandey/AbhiiishekPandey.git
git push -u origin main
```

Then trigger the workflow once by hand from the **Actions** tab
(`workflow_dispatch`) to confirm it commits a fresh heatmap SVG.

## GitHub markdown quirks this repo already works around

- Inline `style="..."` is stripped by GitHub — only `<br>` gives you vertical
  spacing in the README.
- `<h1>`/`<h2>` draw a full-width underline; `<h3>` is used here to avoid it.
- No JavaScript and no external CSS — every animation lives inside its own
  SVG file (SMIL for the ASCII wipe, CSS `@keyframes` for the heatmap).
