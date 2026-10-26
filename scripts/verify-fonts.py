#!/usr/bin/env python3
"""Check the built fonts in fonts/ against their configs.

Usage:
    python3 scripts/verify-fonts.py configs/*.yaml

Exits 1 if any check fails.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

import fontconfig
from fontnames import STYLES, style_file_name

REQUIRED_CODEPOINTS = {
    0x4E2D: "CJK ideograph 中",
    0x3042: "Hiragana あ",
    0xF015: "Nerd Font icon nf-fa-home",
    0xE0B0: "Powerline arrow",
}


def check_font(path, cfg, style):
    errors = []
    font = TTFont(path)
    names = font["name"]
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]

    if names.getDebugName(1) != cfg["family"]:
        errors.append(f"family name is {names.getDebugName(1)!r}")
    if names.getDebugName(2) != style:
        errors.append(f"style name is {names.getDebugName(2)!r}")
    for record in names.names:
        if record.nameID in (1, 2, 3, 4, 6, 16, 17) and "Nerd" in record.toUnicode():
            errors.append(f"name {record.nameID} still says {record.toUnicode()!r}")

    for cp, label in REQUIRED_CODEPOINTS.items():
        if cp not in cmap:
            errors.append(f"missing {label} (U+{cp:04X})")

    cell = hmtx["space"][0]
    ascii_widths = {hmtx[cmap[cp]][0] for cp in range(0x20, 0x7F) if cp in cmap}
    if cfg["mono"]:
        if font["post"].isFixedPitch != 1:
            errors.append("post.isFixedPitch is not 1")
        if font["head"].flags & (1 << 4):
            errors.append("head.flags bit 4 is set")
        if ascii_widths != {cell}:
            errors.append(f"ASCII advances are {sorted(ascii_widths)}, expected {cell}")
        if 0x4E2D in cmap and hmtx[cmap[0x4E2D]][0] != 2 * cell:
            errors.append(f"CJK advance is {hmtx[cmap[0x4E2D]][0]}, expected {2 * cell}")
    else:
        if font["post"].isFixedPitch != 0:
            errors.append("post.isFixedPitch is not 0")
        if len(ascii_widths) < 2:
            errors.append("ASCII advances are all equal; expected a proportional font")

    return errors


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)

    failed = False
    for config_path in sys.argv[1:]:
        cfg = fontconfig.load(config_path)
        out_dir = Path("fonts") / cfg["compact"]
        family_ok = True
        for style in STYLES:
            path = out_dir / style_file_name(cfg["compact"], style)
            errors = [f"{path} not found"] if not path.is_file() else check_font(path, cfg, style)
            for error in errors:
                print(f"✗ {path.name}: {error}")
            family_ok &= not errors
        failed |= not family_ok
        if family_ok:
            print(f"✓ {cfg['family']}: 4 styles verified ({'mono' if cfg['mono'] else 'proportional'})")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
