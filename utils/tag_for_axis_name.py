
def tagForAxisName(name):
    # try to find or make a tag name for this axis name
    names = {
        "weight": ("wght", dict(en="Weight")),
        "width": ("wdth", dict(en="Width")),
        "optical": ("opsz", dict(en="Optical Size")),
        "slant": ("slnt", dict(en="Slant")),
        "italic": ("ital", dict(en="Italic")),
    }
    if name.lower() in names:
        return names[name.lower()]
    if len(name) < 4:
        tag = name + "*" * (4 - len(name))
    else:
        tag = name[:4]
    return tag, dict(en=name)

