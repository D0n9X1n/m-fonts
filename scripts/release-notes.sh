#!/usr/bin/env bash
# release-notes.sh — Print GitHub release notes for a tag
#
# Usage:
#   ./scripts/release-notes.sh <tag> <dist_dir>
#
# Needs full history and tags (fetch-depth: 0) to find the previous release.

set -euo pipefail
cd "$(dirname "$0")/.."

TAG="${1:?usage: $0 <tag> <dist_dir>}"
DIST="${2:?usage: $0 <tag> <dist_dir>}"
REPO="${GITHUB_REPOSITORY:-D0n9X1n/rec-mountain-fonts}"
source versions.env

if [ ! -f "$DIST/SHA256SUMS.txt" ]; then
    echo "ERROR: $DIST/SHA256SUMS.txt not found — run ./scripts/package-release.sh first" >&2
    exit 1
fi
previous=$(git describe --tags --abbrev=0 "${TAG}^" 2> /dev/null || true)

echo "# Rec Mountain Fonts ${TAG}"
echo
echo "| Family | Spacing |"
echo "|---|---|"
# Mono families first, then proportional sans, then serif
for want in 1:recursive 0:recursive 0:anthropic-serif; do
    for cfg in configs/*.yaml; do
        (
            eval "$(python3 scripts/fontconfig.py "$cfg")"
            [ "${MONO}:${BASE}" = "$want" ] || exit 0
            if [ "$MONO" = 1 ]; then
                echo "| **${FAMILY}** | Monospace, code ligatures |"
            elif [ "$BASE" = anthropic-serif ]; then
                echo "| **${FAMILY}** | Proportional serif |"
            else
                echo "| **${FAMILY}** | Proportional |"
            fi
        )
    done
done
echo
echo "Built from Recursive ${RECURSIVE_VERSION}, Anthropic Serif ${ANTHROPIC_SERIF_VERSION}, Resource Han Rounded ${RESOURCE_HAN_ROUNDED_VERSION}, and Nerd Fonts ${NERD_FONTS_VERSION}."
echo
echo "## Install"
echo
echo "Download the \`.ttf\` files or \`rec-mountain-fonts-${TAG}.zip\` below. See [Installation](https://github.com/${REPO}/wiki/Installation)."
echo
echo "## Changes"
echo
if [ -n "$previous" ]; then
    git log --no-merges --format='- %s (%h)' "${previous}..${TAG}"
else
    echo "- First release."
fi
echo
echo "## Checksums"
echo
echo '```text'
cat "$DIST/SHA256SUMS.txt"
echo '```'
