#!/usr/bin/env bash
# Run every solution notebook in the container, so teacher/solutions/ contains the
# expected outputs. Fails if any cell gives an error.
set -euo pipefail
cd "$(dirname "$0")/.."
image="$(docker compose config --images)"
docker run --rm -u root -e NB_UID="$(id -u)" -e NB_GID="$(id -g)" \
    -v "$PWD/teacher:/home/jovyan/teacher" "$image" \
    bash -c 'cd teacher/solutions && status=0
             for f in en/*.ipynb de/*.ipynb; do
               if jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 "$f" >/dev/null 2>&1
               then echo "ok   $f"; else echo "FAIL $f"; status=1; fi
             done
             exit $status' 2>&1 | grep -E '^(ok|FAIL)'
