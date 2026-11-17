#!/usr/bin/env bash
set -euo pipefail
echo 'Public deployment is disabled. GaussLearner is private and preview-only.' >&2
echo 'Preview: python3 -m http.server 8873 --directory /data/gxlh_data/Surmount/GaussLearner' >&2
exit 1
