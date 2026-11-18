# GaussLearner project website

**GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners**

Official website: https://gaoxiang-linghu.github.io/GaussLearner/

## Authors

Gaoxiang Linghu, Haonan Zhou, Xuanhe Liu, Weili Xu, Kaiyue Zhou*, Jun Xiao, Gaoang Wang*.

*Corresponding authors: Kaiyue Zhou and Gaoang Wang.*

Affiliations follow the paper. The website and publicity video title card reflect the authors' updated correspondence designation.

## Website content

This repository contains only website source and presentation assets. No algorithm implementation, dataset, training checkpoint, manuscript PDF or manuscript LaTeX source is included. Paper and Code are placeholders until those resources are released.

## Preview

```bash
python3 -m http.server 8873 --directory /data/gxlh_data/Surmount/GaussLearner
```

For remote preview, forward port 8873 over SSH. The static page needs no dependencies or build step.

## Deployment

The included GitHub Actions workflow stages only HTML, CSS, JavaScript, citation.bib, .nojekyll and assets. Repository visibility is not changed by any script. Publishing the repository and enabling GitHub Pages require an explicit owner decision.

The standalone helper does not upload files or change visibility. GitHub Pages is configured for this repository, and pushes to main deploy reviewed website updates automatically.

## Asset preparation

- scripts/build_page.py: exports paper figures using their authored PDF CropBox, extracts captions and the three main result tables. Requires Python 3, Pillow, Poppler and the local manuscript directory, which is not included in this repository.
- scripts/build_public_video.py: replaces the four-second title card and retains the submission video's soundtrack and comparison content. Requires Python 3, Pillow, FFmpeg and the original local video, which is not included here.
- assets/figures/manifest.json: figure provenance and captions.
- ASSETS.md: video processing and attribution.
