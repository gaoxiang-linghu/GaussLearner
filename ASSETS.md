# Asset provenance

## Manuscript

All 11 displayed figures are exported from Paper/arxiv_camera_v1/figures/. Exact PDF paths, captions and output dimensions are in assets/figures/manifest.json. The three result tables are generated from sec/4_experiments.tex, retaining numerical values and bold/underline emphasis. LaTeX citation markers are omitted in captions. Figure exports use the PDF’s authored CropBox, matching the crop used by LaTeX, rather than the larger MediaBox. This removes only material outside the existing crop; no comparison content or labels are edited.

## Author links and affiliations

Gaoang Wang links to https://cvnext.github.io/ in the same text color as all other authors. Affiliations follow the manuscript. No institution logos or separate Minto wordmark are displayed on the website or publicity title card, following the user's latest instruction.

## Video

assets/video/GaussLearner_public.mp4 is copied from outputs/video/video_publicity/GaussLearner_public.mp4. Its source is outputs/video/sup_submission/GaussLearner_full.mp4.

Only the initial four-second title card is replaced. Comparison frames, explanations, narration, ending card and soundtrack are retained. The audio stream is copied without re-encoding. The submission video is unchanged.

The inherited ApartmentRoom CL-Splats display-only filtering is documented in outputs/video/sup_submission/sources/apartmentroom_clsplats_display_filter.json. It suppresses 6,747 extreme Gaussians with a fixed union mask across the clip; checkpoints and quantitative metrics are unchanged. This policy is inherited with no further filtering or enhancement.

Music: **First Snow — Scott Buckley**  
https://www.scottbuckley.com.au/library/first-snow/  
Creative Commons Attribution 4.0: https://creativecommons.org/licenses/by/4.0/

The original ending card retains the visible music credit. Music was trimmed, normalized, faded and ducked under narration in the source video. Include the attribution in the description if uploading to a video platform.

## Website

The HTML, CSS and JavaScript are written for this project. Layout references: IGFuse, LightFuse, GaussianUpdate and CL-Splats. No template implementation or third-party JavaScript is copied.
