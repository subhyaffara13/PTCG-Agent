import re

def replaceFn(match: re.Match[str]) -> str:
    return SCOPED_ABBR[match.group(1).lower()]

