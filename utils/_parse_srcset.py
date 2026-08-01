
def _parse_srcset(entries):
    """
    Parse srcset for multiples...
    """
    srcset = {}
    for entry in entries:
        entry = entry.strip()
        if len(entry) >= 2:
            mult = entry[:-1]
            srcset[float(mult)] = entry
        else:
            raise ExtensionError(f'srcset argument {entry!r} is invalid.')
    return srcset

