#!/usr/bin/env bash
# fetch-sources.sh — Download the pinned upstream sources into sources/
#
# Usage:
#   ./scripts/fetch-sources.sh
#
# Versions come from versions.env. A source is downloaded again only when its
# pinned version changes.

set -euo pipefail
cd "$(dirname "$0")/.."
source versions.env

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# current <dir> <version> — succeeds if <dir> already holds <version>
current() { [ "$(cat "$1/.version" 2>/dev/null)" = "$2" ]; }

# ── Recursive variable font + code ligature feature file ──
dir="sources/recursive"
if ! current "$dir" "$RECURSIVE_VERSION"; then
    echo "Fetching Recursive v${RECURSIVE_VERSION}..."
    rm -rf "$dir" && mkdir -p "$dir"
    curl -fsSL -o "$TMP/recursive.zip" \
        "https://github.com/arrowtype/recursive/releases/download/v${RECURSIVE_VERSION}/ArrowType-Recursive-${RECURSIVE_VERSION}.zip"
    unzip -q -j "$TMP/recursive.zip" "*/Recursive_Desktop/Recursive_VF_${RECURSIVE_VERSION}.ttf" -d "$dir"
    curl -fsSL -o "$dir/calt-generated--code_fonts_only.fea" \
        "https://raw.githubusercontent.com/arrowtype/recursive/v${RECURSIVE_VERSION}/src/features/features/calt-generated--code_fonts_only.fea"
    echo "$RECURSIVE_VERSION" > "$dir/.version"
fi

# ── Resource Han Rounded CN (Regular + Bold) ──
dir="sources/resource-han-rounded"
if ! current "$dir" "$RESOURCE_HAN_ROUNDED_VERSION"; then
    echo "Fetching Resource Han Rounded v${RESOURCE_HAN_ROUNDED_VERSION}..."
    SEVENZIP=$(command -v 7z || command -v 7zz || true)
    if [ -z "$SEVENZIP" ]; then
        echo "ERROR: 7z not found (brew install sevenzip / apt-get install p7zip-full)" >&2
        exit 1
    fi
    rm -rf "$dir" && mkdir -p "$dir"
    curl -fsSL -o "$TMP/rhr.7z" \
        "https://github.com/CyanoHao/Resource-Han-Rounded/releases/download/v${RESOURCE_HAN_ROUNDED_VERSION}/RHR-CN-${RESOURCE_HAN_ROUNDED_VERSION}.7z"
    "$SEVENZIP" x -o"$TMP/rhr" "$TMP/rhr.7z" > /dev/null
    for weight in Regular Bold; do
        src=$(find "$TMP/rhr" -name "ResourceHanRoundedCN-${weight}.ttf" | head -1)
        if [ -z "$src" ]; then
            echo "ERROR: ResourceHanRoundedCN-${weight}.ttf not found in archive" >&2
            exit 1
        fi
        cp "$src" "$dir/"
    done
    echo "$RESOURCE_HAN_ROUNDED_VERSION" > "$dir/.version"
fi

# ── Nerd Fonts patcher ──
dir="sources/nerd-fonts-patcher"
if ! current "$dir" "$NERD_FONTS_VERSION"; then
    echo "Fetching Nerd Fonts patcher v${NERD_FONTS_VERSION}..."
    rm -rf "$dir" && mkdir -p "$dir"
    curl -fsSL -o "$TMP/patcher.zip" \
        "https://github.com/ryanoasis/nerd-fonts/releases/download/v${NERD_FONTS_VERSION}/FontPatcher.zip"
    unzip -q "$TMP/patcher.zip" -d "$dir"
    echo "$NERD_FONTS_VERSION" > "$dir/.version"
fi

echo "Sources: Recursive ${RECURSIVE_VERSION}, Resource Han Rounded ${RESOURCE_HAN_ROUNDED_VERSION}, Nerd Fonts ${NERD_FONTS_VERSION}"
