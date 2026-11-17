# GaussLearner — private preview

Static website for **GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners**.

## Visibility

The repository leo4384509/GaussLearner is private. Public deployment is disabled. The GitHub Pages workflow is removed, and scripts/publish_github.sh stops immediately without changing GitHub or uploading files. Keep this state until the owner explicitly requests publication.

## Preview

```bash
python3 -m http.server 8873 --directory /data/gxlh_data/Surmount/GaussLearner
```

For a preview accessible only on the server itself, add --bind 127.0.0.1 and use an SSH tunnel. The existing preview uses the server's private network address so the owner can review it in the app.

No dependency installation, CDN, backend or build is required. Assets use relative paths.

## Content and maintenance

The repository contains website assets only: no algorithm code, datasets, checkpoints, manuscript sources or manuscript PDFs. Paper and Code remain placeholders. No arXiv identifier or conference venue has been invented.

- scripts/build_page.py exports manuscript figures, captions and three main result tables. Requires Python 3, Pillow, Poppler and ../Paper/arxiv_camera_v1, or an explicit manuscript directory argument.
- scripts/build_public_video.py prepares the title card and video. Requires Python 3, Pillow, FFmpeg and original assets in the parent workspace. The publicity filename denotes intended future use; the file is not currently published.
- assets/figures/manifest.json records figure provenance and captions.
- ASSETS.md documents video processing and attribution.

Preparation scripts are not required to view the local website.
