#!/usr/bin/env python3
"""Load a family config from configs/*.yaml.

A config can start from another with `Extends: <file>`; its own keys replace
the parent's. `Exclude Features` removes entries from the inherited `Features`.

`Base` picks the Latin source: `recursive` (the default) instantiates styles
from the Recursive variable font by axis values; `anthropic-serif` takes each
style from a static Anthropic Serif Text weight and is always proportional.

Run as a script, it prints shell assignments for build.sh:

    eval "$(python3 scripts/fontconfig.py configs/st-helens.yaml)"
    # sets FAMILY, COMPACT, MONO (1 or 0), BASE
"""

import shlex
import sys
from pathlib import Path

import yaml

STYLES = ("Regular", "Italic", "Bold", "Bold Italic")
STYLE_AXES = ("CASL", "wght", "slnt", "CRSV")
BASES = ("recursive", "anthropic-serif")
# Anthropic Serif Text weights fetched by fetch-sources.sh
SERIF_WEIGHTS = ("Regular", "RegularItalic", "Semibold", "SemiboldItalic")


def read(path):
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    parent = cfg.pop("Extends", None)
    if parent:
        cfg = {**read(path.parent / parent), **cfg}
    return cfg


def load(path):
    cfg = read(path)
    family = cfg["Family Name"]
    base = cfg.get("Base", "recursive")
    if base not in BASES:
        raise ValueError(f"{path}: Base must be one of: {', '.join(BASES)}")
    mono = bool(cfg["Mono"])
    if base == "anthropic-serif" and mono:
        raise ValueError(f"{path}: an anthropic-serif family must have Mono: false")

    styles = cfg["Styles"]
    if set(styles) != set(STYLES):
        raise ValueError(f"{path}: Styles must be exactly: {', '.join(STYLES)}")
    for style in STYLES:
        if base == "recursive":
            missing = set(STYLE_AXES) - set(styles[style])
            if missing:
                raise ValueError(f"{path}: {style} is missing {', '.join(sorted(missing))}")
        elif styles[style] not in SERIF_WEIGHTS:
            raise ValueError(f"{path}: {style} must be one of: {', '.join(SERIF_WEIGHTS)}")
    axes = {style: {**styles[style], "MONO": 1 if mono else 0} for style in STYLES} if base == "recursive" else None
    sources = {style: styles[style] for style in STYLES} if base == "anthropic-serif" else None

    features = list(cfg.get("Features") or [])
    excluded = list(cfg.get("Exclude Features") or [])
    unknown = sorted(set(excluded) - set(features))
    if unknown:
        raise ValueError(f"{path}: Exclude Features lists features that are not enabled: {', '.join(unknown)}")

    return {
        "family": family,
        "compact": family.replace(" ", ""),
        "base": base,
        "mono": mono,
        # Code ligatures are re-spaced onto the mono cell grid (see dlig2calt.py),
        # which would squash every glyph wider than a space in a proportional font.
        "ligatures": mono and bool(cfg.get("Code Ligatures", False)),
        "features": [f for f in features if f not in excluded],
        "axes": axes,
        "sources": sources,
    }


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    cfg = load(sys.argv[1])
    print(f"FAMILY={shlex.quote(cfg['family'])}")
    print(f"COMPACT={shlex.quote(cfg['compact'])}")
    print(f"MONO={1 if cfg['mono'] else 0}")
    print(f"BASE={shlex.quote(cfg['base'])}")


if __name__ == "__main__":
    main()
