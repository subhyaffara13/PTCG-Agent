import re

def strip_quotes(s: str) -> str:
    """Strip a double quote at the beginning and end of the string, if any."""
    s = re.sub('^"', "", s)
    s = re.sub('"$', "", s)
    return s

