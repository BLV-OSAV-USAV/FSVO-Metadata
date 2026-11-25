#!/usr/bin/env bash
set -euo pipefail

source_log=$1
harvester=$2
environment=$3
log_dir="logs/i14y/$harvester/$environment"
log_path="$log_dir/latest.txt"

mkdir -p "$log_dir"
{
  printf 'GitHub Actions run %s (attempt %s)\n\n' "$GITHUB_RUN_ID" "$GITHUB_RUN_ATTEMPT"
  cat "$source_log"
} > "$log_path"
git add -- "$log_path"
if git diff --cached --quiet -- "$log_path"; then
  exit 0
fi

git -c user.name='github-actions[bot]' \
  -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
  commit -m "Add I14Y $harvester $environment harvest log" -- "$log_path"

for attempt in 1 2 3; do
  if git push origin "HEAD:$GITHUB_REF"; then
    exit 0
  fi
  if [[ "$attempt" == 3 ]]; then
    exit 1
  fi
  git fetch origin "$GITHUB_REF"
  git -c user.name='github-actions[bot]' \
    -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
    rebase -X theirs FETCH_HEAD
done
