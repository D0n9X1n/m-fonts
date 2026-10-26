"""Turn Recursive's code ligatures on by default by moving them from dlig to calt.

Recursive draws code ligatures (=>, !=, ...) as glyphs wider than one cell. For
mono fonts each wide glyph is given a one-cell advance with its outline shifted
left, so it overhangs the cells before it and the text stays on the grid.
"""

from fontTools import ttLib
from fontTools.feaLib import builder


def dlig2calt(font_path, fea_path):
    font = ttLib.TTFont(font_path)
    glyf, hmtx = font["glyf"], font["hmtx"]
    cell = hmtx["space"][0]

    # The calt feature substitutes LIG, an empty one-cell glyph, as a placeholder
    glyf["LIG"] = glyf["space"]
    hmtx["LIG"] = hmtx["space"]

    for name in font.getGlyphNames():
        width, lsb = hmtx[name]
        if width <= cell:
            continue

        overhang = width - cell
        hmtx[name] = (cell, lsb - overhang)

        # Shift the outline left; replace the phantom points (the last four
        # coordinates) so _setCoordinates writes back a one-cell advance.
        coords = glyf._getCoordinatesAndControls(name, hmtx.metrics)[0]
        phantoms = glyf._getPhantomPoints(name, hmtx.metrics)
        shifted = [(x - overhang, y) for x, y in coords[: len(coords) - 4]]
        new_phantoms = [(0, 0), (cell, 0), phantoms[-2], phantoms[-1]]
        glyf._setCoordinates(name, shifted + new_phantoms, hmtx.metrics)

    builder.addOpenTypeFeatures(font, fea_path)
    font.save(font_path)
