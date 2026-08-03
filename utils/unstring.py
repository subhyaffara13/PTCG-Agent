import re

def unstring(obj):
    """
    Attempt to parse string to native integer formats.
    One can't simply call int/float in a try/catch because there is a
    semantic difference between (for example) 15.0 and 15.
    """
    floatreg = "^\\d+.\\d+$"
    match = re.findall(floatreg, obj)
    if match != []:
        return float(match[0])

    intreg = "^\\d+$"
    match = re.findall(intreg, obj)
    if match != []:
        return int(match[0])
    return obj

