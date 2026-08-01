
def parseLookupFlags(lines):
    flags = 0
    filterset = None
    allFlags = [
        "righttoleft",
        "ignorebaseglyphs",
        "ignoreligatures",
        "ignoremarks",
        "markattachmenttype",
        "markfiltertype",
    ]
    while lines.peeks()[0].lower() in allFlags:
        line = next(lines)
        flag = {
            "righttoleft": 0x0001,
            "ignorebaseglyphs": 0x0002,
            "ignoreligatures": 0x0004,
            "ignoremarks": 0x0008,
        }.get(line[0].lower())
        if flag:
            assert line[1].lower() in ["yes", "no"], line[1]
            if line[1].lower() == "yes":
                flags |= flag
            continue
        if line[0].lower() == "markattachmenttype":
            flags |= int(line[1]) << 8
            continue
        if line[0].lower() == "markfiltertype":
            flags |= 0x10
            filterset = int(line[1])
    return flags, filterset

