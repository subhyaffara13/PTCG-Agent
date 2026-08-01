
def parseTable(lines, font, tableTag=None):
    log.debug("Parsing table")
    line = lines.peeks()
    tag = None
    if line[0].split()[0] == "FontDame":
        tag = line[0].split()[1]
    elif " ".join(line[0].split()[:3]) == "Font Chef Table":
        tag = line[0].split()[3]
    if tag is not None:
        next(lines)
        tag = tag.ljust(4)
        if tableTag is None:
            tableTag = tag
        else:
            assert tableTag == tag, (tableTag, tag)

    assert (
        tableTag is not None
    ), "Don't know what table to parse and data doesn't specify"

    return {
        "GSUB": parseGSUB,
        "GPOS": parseGPOS,
        "GDEF": parseGDEF,
        "cmap": parseCmap,
    }[tableTag](lines, font)

