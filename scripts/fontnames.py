"""Name-table helpers shared by the build stages, so every stage names fonts the same way."""

STYLES = ("Regular", "Italic", "Bold", "Bold Italic")


def style_file_name(compact, style):
    return f"{compact}-{style.replace(' ', '')}.ttf"


def style_from_flags(font):
    """Read the RIBBI style back from head.macStyle (bit 0 bold, bit 1 italic)."""
    mac_style = font["head"].macStyle
    return STYLES[(2 if mac_style & 1 else 0) + (1 if mac_style & 2 else 0)]


def set_names(font, family, style):
    """Write family, style, full, PostScript and unique names for a RIBBI font."""
    compact = family.replace(" ", "")
    ps_name = f"{compact}-{style.replace(' ', '')}"
    full_name = family if style == "Regular" else f"{family} {style}"
    unique_id = f"{font['head'].fontRevision:.3f};{ps_name}"

    name = font["name"]
    # 16/17 (typographic family/subfamily) are unneeded for a 4-style RIBBI family,
    # and 25 (variations PostScript prefix) is meaningless once instantiated.
    for name_id in (1, 2, 3, 4, 6, 16, 17, 25):
        name.removeNames(nameID=name_id)
    for name_id, value in {1: family, 2: style, 3: unique_id, 4: full_name, 6: ps_name}.items():
        name.setName(value, name_id, 3, 1, 0x409)  # Windows, Unicode BMP, en-US
        name.setName(value, name_id, 1, 0, 0)  # Mac, Roman, English
