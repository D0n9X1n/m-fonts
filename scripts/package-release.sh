#!/usr/bin/env bash
# package-release.sh — Collect built fonts into dist/ for a GitHub release
#
# Usage:
#   ./scripts/package-release.sh <tag>
#
# Writes dist/*.ttf, dist/m-fonts-<tag>.zip, and dist/SHA256SUMS.txt.

set -euo pipefail
cd "$(dirname "$0")/.."

TAG="${1:?usage: $0 <tag>}"
CONFIGS=(configs/*.yaml)
EXPECTED=$(( ${#CONFIGS[@]} * 4 ))

shopt -s nullglob
fonts=(fonts/*/*.ttf)
if [ "${#fonts[@]}" -ne "$EXPECTED" ]; then
    echo "ERROR: expected ${EXPECTED} fonts in fonts/, found ${#fonts[@]} — run ./scripts/build-all.sh" >&2
    exit 1
fi

rm -rf dist
mkdir -p dist
cp "${fonts[@]}" dist/

(
    cd dist
    zip -q -X "m-fonts-${TAG}.zip" ./*.ttf
    if command -v sha256sum > /dev/null; then
        sha256sum ./*.ttf ./*.zip | sed 's| \./| |' > SHA256SUMS.txt
    else
        shasum -a 256 ./*.ttf ./*.zip | sed 's| \./| |' > SHA256SUMS.txt
    fi
)
ls -lh dist
