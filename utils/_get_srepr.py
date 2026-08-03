import re

def _get_srepr(expr):
    s = srepr(expr)
    s = re.sub(r"WildDot\('(\w+)'\)", r"\1", s)
    s = re.sub(r"WildPlus\('(\w+)'\)", r"*\1", s)
    s = re.sub(r"WildStar\('(\w+)'\)", r"*\1", s)
    return s

