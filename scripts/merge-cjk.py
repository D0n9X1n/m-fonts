"""Stage 2: merge CJK glyphs from Resource Han Rounded into a Rec Mountain font.

Run with FontForge's Python:
    fontforge -script scripts/merge-cjk.py <target.ttf> <cjk.ttf> <output.ttf> [--scale 1.1] [--proportional]

CJK glyphs are scaled to fit the target's typo ascender/descender (then by
--scale), centred vertically on that body and horizontally in their advance.
Mono fonts get exact cell widths: two cells for full-width forms, one for
halfwidth forms. Proportional fonts keep each glyph's own advance, scaled.
"""

import argparse

import fontforge

DOUBLE_WIDTH_RANGES = [
    (0x2E80, 0x2EFF), (0x2F00, 0x2FDF), (0x3000, 0x303F),
    (0x3040, 0x309F), (0x30A0, 0x30FF), (0x3100, 0x312F),
    (0x3130, 0x318F), (0x31A0, 0x31BF), (0x31F0, 0x31FF),
    (0x3200, 0x32FF), (0x3300, 0x33FF), (0x3400, 0x4DBF),
    (0x4DC0, 0x4DFF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
    (0xFE30, 0xFE4F), (0xFF01, 0xFF60), (0xFFE0, 0xFFE6),
]

HALFWIDTH_RANGES = [
    (0xFF61, 0xFF9F), (0xFFA0, 0xFFDC), (0xFFE8, 0xFFEF),
]

# Common ideographs used to measure the CJK font's vertical extent
SAMPLE_CODEPOINTS = [0x4E2D, 0x6587, 0x5B57, 0x4EBA, 0x5927, 0x5C0F, 0x56FD, 0x7684]


def cjk_vertical_bounds(source):
    boxes = [source[cp].boundingBox() for cp in SAMPLE_CODEPOINTS if cp in source]
    if not boxes:
        raise SystemExit("CJK source has none of the sample ideographs")
    return min(b[1] for b in boxes), max(b[3] for b in boxes)


def merge_cjk(target_path, cjk_path, output_path, scale, proportional):
    target = fontforge.open(target_path)
    source = fontforge.open(cjk_path)

    cell = target[0x20].width
    ascent, descent = target.os2_typoascent, target.os2_typodescent
    em_scale = float(target.em) / source.em

    # Shrink to fit the target's line body if needed, then apply the user scale
    ymin, ymax = cjk_vertical_bounds(source)
    fit = min(1.0, (ascent - descent) / ((ymax - ymin) * em_scale))
    total_scale = em_scale * fit * scale
    v_offset = (ascent + descent) / 2.0 - (ymin + ymax) * total_scale / 2.0
    print("Scale: %.4f (cjk scale %.2f), v_offset: %.1f, %s" % (
        total_scale, scale, v_offset, "proportional" if proportional else "cell %d" % cell))

    double_width = {cp for start, end in DOUBLE_WIDTH_RANGES for cp in range(start, end + 1)}
    merged = 0
    for start, end in DOUBLE_WIDTH_RANGES + HALFWIDTH_RANGES:
        for cp in range(start, end + 1):
            if cp not in source or not source[cp].isWorthOutputting():
                continue
            source.selection.select(cp)
            source.copy()
            target.selection.select(cp)
            target.paste()

            glyph = target[cp]
            if proportional:
                width = int(round(source[cp].width * total_scale))
            else:
                width = cell * 2 if cp in double_width else cell

            glyph.transform((total_scale, 0, 0, total_scale, 0, v_offset))
            xmin, _, xmax, _ = glyph.boundingBox()
            if xmax > xmin:
                glyph.transform((1, 0, 0, 1, width / 2.0 - (xmin + xmax) / 2.0, 0))
            glyph.width = width
            merged += 1

    # Advertise the Japanese (JIS) and Simplified Chinese code pages
    target.os2_codepages = (target.os2_codepages[0] | (1 << 17) | (1 << 18), target.os2_codepages[1])
    target.generate(output_path)
    print("Merged %d CJK glyphs → %s" % (merged, output_path))
    target.close()
    source.close()


def main():
    parser = argparse.ArgumentParser(description="Merge CJK glyphs into a Rec font.")
    parser.add_argument("target")
    parser.add_argument("cjk")
    parser.add_argument("output")
    parser.add_argument("--scale", type=float, default=1.0, help="CJK size multiplier (e.g. 1.1)")
    parser.add_argument("--proportional", action="store_true", help="keep proportional CJK advances")
    args = parser.parse_args()
    merge_cjk(args.target, args.cjk, args.output, args.scale, args.proportional)


if __name__ == "__main__":
    main()
