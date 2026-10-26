#!/usr/bin/env python3
"""Stage 1: instantiate the four static styles from the Recursive variable font.

Usage:
    python3 scripts/instantiate-fonts.py <config.yaml> <Recursive_VF.ttf> <calt.fea> <output_dir>
"""

import logging
import sys
from pathlib import Path

import ttfautohint
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.varLib.instancer import OverlapMode
from opentype_feature_freezer import cli as pyftfeatfreeze

import fontconfig
from dlig2calt import dlig2calt
from fontnames import STYLES, set_names, style_file_name

# opentype_feature_freezer warns about every lookup it can't remap
logging.getLogger("opentype_feature_freezer").setLevel(logging.ERROR)

MONO_CELL = 600  # Recursive's mono advance width at UPM 1000


def set_spacing(font, mono):
    post, os2 = font["post"], font["OS/2"]
    if mono:
        post.isFixedPitch = 1
        os2.panose.bProportion = 9  # Monospaced
        os2.xAvgCharWidth = MONO_CELL  # the computed average is skewed by wide ligature glyphs
    else:
        post.isFixedPitch = 0
        os2.panose.bProportion = 0  # Any
        os2.recalcAvgCharWidth(font)


def set_style_flags(font, style):
    """Set RIBBI style linking bits (adapted from gftools fix_fs_selection)."""
    bold = style.startswith("Bold")
    italic = style.endswith("Italic")
    os2 = font["OS/2"]

    fs_selection = os2.fsSelection & (1 << 7)  # keep only USE_TYPO_METRICS
    if italic:
        fs_selection |= 1 << 0
    if bold:
        fs_selection |= 1 << 5
    if not (bold or italic):
        fs_selection |= 1 << 6  # REGULAR
    os2.fsSelection = fs_selection

    font["head"].macStyle = (0b01 if bold else 0) | (0b10 if italic else 0)
    if italic:
        os2.panose.bLetterForm = 11  # Oblique/Boxed


def build_style(cfg, varfont, fea_path, style, out_path):
    font = instancer.instantiateVariableFont(varfont, cfg["axes"][style], overlap=OverlapMode.REMOVE)
    del font["STAT"]  # STAT overrides RIBBI style linking on Windows
    set_names(font, cfg["family"], style)
    font.save(out_path)

    # Freeze rvrn (glyph swaps at these axis values) and the chosen stylistic sets
    features = ",".join(["rvrn"] + cfg["features"])
    pyftfeatfreeze.main([f"--features={features}", str(out_path), str(out_path)])

    if cfg["ligatures"]:
        dlig2calt(str(out_path), fea_path)

    font = TTFont(out_path)
    set_spacing(font, cfg["mono"])
    set_style_flags(font, style)
    font.save(out_path)

    ttfautohint.ttfautohint(in_file=str(out_path), out_file=str(out_path), hint_composites=True)


def main():
    if len(sys.argv) != 5:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    config_path, varfont_path, fea_path, out_dir = sys.argv[1:]
    cfg = fontconfig.load(config_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    varfont = TTFont(varfont_path)
    for style in STYLES:
        out_path = out_dir / style_file_name(cfg["compact"], style)
        build_style(cfg, varfont, fea_path, style, out_path)
        print(f"  {style} → {out_path}")


if __name__ == "__main__":
    main()
