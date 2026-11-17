#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
command -v gh >/dev/null || { echo 'Install GitHub CLI and authenticate as leo4384509 first.' >&2; exit 1; }
account=$(gh api user --jq .login)
[[ "$account" == leo4384509 ]] || { echo "Expected leo4384509; current account: $account" >&2; exit 1; }
repo=leo4384509/GaussLearner
if ! gh repo view "$repo" >/dev/null 2>&1; then
  result=$(gh api --include "repos/$repo" 2>&1 || true)
  [[ "$result" == *'HTTP/2.0 404'* || "$result" == *'HTTP/1.1 404'* || "$result" == *'HTTP 404'* ]] || { echo "$result" >&2; exit 1; }
  gh repo create "$repo" --public --description 'Project page for GaussLearner: 3D Gaussian Primitives as Self-Regulating Continual Learners'
fi
gh auth setup-git
remote_head=$(git ls-remote "https://github.com/$repo.git" HEAD | cut -f1)
if [[ -n "$remote_head" && "$remote_head" != "$(git rev-parse HEAD)" ]]; then
  echo 'Remote repository has existing content. Review and reconcile before publishing.' >&2
  exit 1
fi
if git remote get-url origin >/dev/null 2>&1; then
  [[ "$(git remote get-url origin)" == "https://github.com/$repo.git" ]] || { echo 'Unexpected origin; refusing to change it.' >&2; exit 1; }
else
  git remote add origin "https://github.com/$repo.git"
fi
git push -u origin main
pages=$(gh api "repos/$repo/pages" --jq .build_type 2>/dev/null || true)
if [[ -z "$pages" ]]; then
  gh api --method POST "repos/$repo/pages" -f build_type=workflow >/dev/null
elif [[ "$pages" != workflow ]]; then
  gh api --method PUT "repos/$repo/pages" -f build_type=workflow >/dev/null
fi
gh workflow run pages.yml --repo "$repo" --ref main
echo 'Deployment: https://github.com/leo4384509/GaussLearner/actions'
echo 'Target URL after deployment: https://leo4384509.github.io/GaussLearner/'
