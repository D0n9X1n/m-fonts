#!/usr/bin/env python3
"""Stage 1: make the four static styles from the config's Latin source.

Usage:
    python3 scripts/instantiate-fonts.py <config.yaml> <Recursive_VF.ttf> <calt.fea> <output_dir>
    python3 scripts/instantiate-fonts.py <config.yaml> <anthropic_serif_dir> <output_dir>

Recursive families are instantiated from the variable font. Anthropic Serif
families take each style from a static CFF font, converted to TrueType outlines
at UPM 1000 so the CJK merge and the Nerd Fonts patcher see the same layout as
the Recursive families.
"""

import logging
import sys
from pathlib import Path

import ttfautohint
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools.varLib import instancer
from fontTools.varLib.instancer import OverlapMode
from opentype_feature_freezer import cli as pyftfeatfreeze

import fontconfig
from dlig2calt import dlig2calt
from fontnames import STYLES, set_names, style_file_name

# opentype_feature_freezer warns about every lookup it can't remap
logging.getLogger("opentype_feature_freezer").setLevel(logging.ERROR)

MONO_CELL = 600  # Recursive's mono advance width at UPM 1000
UPM = 1000


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


def finish_style(cfg, style, out_path):
    font = TTFont(out_path)
    set_spacing(font, cfg["mono"])
    set_style_flags(font, style)
    font.save(out_path)

    ttfautohint.ttfautohint(in_file=str(out_path), out_file=str(out_path), hint_composites=True)


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

    finish_style(cfg, style, out_path)


def cff_to_glyf(font):
    """Replace CFF outlines with quadratic TrueType outlines (as fontTools' otf2ttf snippet)."""
    glyph_set = font.getGlyphSet()
    glyf = newTable("glyf")
    glyf.glyphOrder = font.getGlyphOrder()
    glyf.glyphs = {}
    for name in glyf.glyphOrder:
        pen = TTGlyphPen(glyph_set)
        glyph_set[name].draw(Cu2QuPen(pen, max_err=1.0, reverse_direction=True))
        glyf[name] = pen.glyph()

    for tag in ("CFF ", "VORG"):
        if tag in font:
            del font[tag]
    font["glyf"] = glyf
    font["loca"] = newTable("loca")
    font["head"].indexToLocFormat = 0
    font["head"].glyphDataFormat = 0
    maxp = font["maxp"]
    maxp.tableVersion = 0x00010000
    for field in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs",
                  "maxStackElements", "maxSizeOfInstructions", "maxComponentElements"):
        setattr(maxp, field, 0)
    maxp.maxZones = 1
    post = font["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    font.sfntVersion = "\0\1\0\0"


def build_serif_style(cfg, source_dir, style, out_path):
    font = TTFont(Path(source_dir) / f"AnthropicSerif-Text-{cfg['sources'][style]}-Static.otf")
    scale_upem(font, UPM)
    cff_to_glyf(font)
    if "STAT" in font:
        del font["STAT"]  # STAT overrides RIBBI style linking on Windows
    set_names(font, cfg["family"], style)
    font.save(out_path)

    if cfg["features"]:
        pyftfeatfreeze.main([f"--features={','.join(cfg['features'])}", str(out_path), str(out_path)])

    finish_style(cfg, style, out_path)


def main():
    cfg = fontconfig.load(sys.argv[1]) if len(sys.argv) > 1 else None
    if cfg is None or len(sys.argv) != (5 if cfg["base"] == "recursive" else 4):
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    out_dir = Path(sys.argv[-1])
    out_dir.mkdir(parents=True, exist_ok=True)

    varfont = TTFont(sys.argv[2]) if cfg["base"] == "recursive" else None
    for style in STYLES:
        out_path = out_dir / style_file_name(cfg["compact"], style)
        if varfont:
            build_style(cfg, varfont, sys.argv[3], style, out_path)
        else:
            build_serif_style(cfg, sys.argv[2], style, out_path)
        print(f"  {style} → {out_path}")


if __name__ == "__main__":
    main()
