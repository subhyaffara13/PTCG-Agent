import re

def remove_numbers(lines):
    def _clean(s):
        return re.sub(r"(?:[\d_]|\*\*)", "", s).strip()

    if isinstance(lines, str):
        return _clean(lines)
    out = []
    for l in lines:
        out.append(_clean(l))
    return out

