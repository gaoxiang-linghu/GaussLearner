# GaussLearner project page

Static website for **GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners**.

Target repository: `leo4384509/GaussLearner`  
Target website: https://leo4384509.github.io/GaussLearner/

## Preview

```bash
python3 -m http.server 8873 --directory /data/gxlh_data/Surmount/GaussLearner
```

No dependency installation, CDN, backend or build is required. Assets use relative paths and support the `/GaussLearner/` subdirectory.

## Publish

Authenticate GitHub CLI as `leo4384509`, then run:

```bash
bash /data/gxlh_data/Surmount/GaussLearner/scripts/publish_github.sh
```

The script creates an empty public repository if necessary, enables GitHub Pages with Actions, and pushes main. It stops for a different authenticated account or existing remote content. The workflow stages only index.html, CSS, JavaScript, citation.bib, .nojekyll and assets.

Alternatively create an empty public GaussLearner repository under leo4384509, push this directory's main branch, and select Settings → Pages → Source → GitHub Actions.

This repository contains website assets only: no algorithm code, datasets, checkpoints, manuscript sources or manuscript PDFs.

## Update arXiv and citation

Replace the disabled Paper button in index.html with an anchor to the verified arXiv URL, preserving class resource and removing its Coming Soon badge. Add the verified identifier and URL to citation.bib and the #bibtex block. Keep scripts/build_page.py synchronized if regenerating the page.

The current @misc citation includes the confirmed title, authors and year without inventing an arXiv ID or conference venue. Code remains Coming Soon until release is authorized.

## Regeneration

- scripts/build_page.py exports manuscript figures, captions and the three main result tables. Requires Python 3, Pillow, Poppler and ../Paper/arxiv_camera_v1, or an explicit manuscript directory argument.
- scripts/build_public_video.py prepares the title card and publicity video. Requires Python 3, Pillow, FFmpeg and the original assets in the parent workspace.
- assets/figures/manifest.json records figure source paths and captions.
- ASSETS.md documents video processing and music attribution.

Preparation scripts are not needed by visitors or GitHub Actions.
