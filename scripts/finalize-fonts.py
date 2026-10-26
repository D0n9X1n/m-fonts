#!/usr/bin/env python3
"""Stage 4: give the patched fonts their final names and spacing flags.

The Nerd Fonts patcher appends "Nerd Font" / "Nerd Font Propo" to the names, so
they are rewritten from the config.

For mono families it also marks the font as not fixed-pitch, because icons and
CJK glyphs are two cells wide. Windows Terminal and DirectWrite read that flag
directly and fall back to per-glyph layout with subpixel advances, so rounding
walks ASCII text off the cell grid. This restores:

- post.isFixedPitch = 1
- OS/2.xAvgCharWidth = the cell width
- head.flags bit 4 cleared ("instructions may alter advance width"); when set,
  DirectWrite lets hinting nudge advances at render time

Usage:
    python3 scripts/finalize-fonts.py <config.yaml> <patched_dir> <output_dir>
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

import fontconfig
from fontnames import STYLES, set_names, style_file_name, style_from_flags

HEAD_FLAG_INSTRUCTIONS_ALTER_ADVANCE = 1 << 4


def fix_mono_flags(font, path):
    cell = font["hmtx"]["space"][0]
    font["post"].isFixedPitch = 1
    font["OS/2"].xAvgCharWidth = cell
    font["head"].flags &= ~HEAD_FLAG_INSTRUCTIONS_ALTER_ADVANCE
    if font["OS/2"].panose.bProportion != 9:
        print(f"  WARN {path.name}: panose.bProportion={font['OS/2'].panose.bProportion}, expected 9",
              file=sys.stderr)


def main():
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    cfg = fontconfig.load(sys.argv[1])
    patched_dir, out_dir = Path(sys.argv[2]), Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    seen = set()
    for path in sorted(patched_dir.glob("*.ttf")):
        font = TTFont(path)
        style = style_from_flags(font)
        if style in seen:
            sys.exit(f"ERROR: two patched fonts have style {style}")
        seen.add(style)

        set_names(font, cfg["family"], style)
        if cfg["mono"]:
            fix_mono_flags(font, path)
        out_path = out_dir / style_file_name(cfg["compact"], style)
        font.save(out_path)
        print(f"  {path.name} → {out_path}")

    if seen != set(STYLES):
        sys.exit(f"ERROR: missing styles: {', '.join(sorted(set(STYLES) - seen))}")


if __name__ == "__main__":
    main()
