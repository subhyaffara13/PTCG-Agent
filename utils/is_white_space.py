
def isWhiteSpace(code: int) -> bool:
    r"""Zs (unicode class) || [\t\f\v\r\n]"""
    if code >= 0x2000 and code <= 0x200A:
        return True
    return code in MD_WHITESPACE

