
def _check_freetype_version(ver):
    if ver is None:
        return True

    if isinstance(ver, str):
        ver = (ver, ver)
    ver = [parse_version(x) for x in ver]
    found = parse_version(ft2font.__freetype_version__)

    return ver[0] <= found <= ver[1]

