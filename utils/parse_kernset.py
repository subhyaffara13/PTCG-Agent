
def parseKernset(lines, font, _lookupMap=None):
    typ = lines.peeks()[0].split()[0].lower()
    if typ in ("left", "right"):
        with lines.until(
            ("firstclass definition begin", "secondclass definition begin")
        ):
            return parsePair(lines, font)
    return parsePair(lines, font)

