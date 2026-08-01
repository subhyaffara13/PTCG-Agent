
def isValidEntityCode(c: int) -> bool:
    # broken sequence
    if c >= 0xD800 and c <= 0xDFFF:
        return False
    # never used
    if c >= 0xFDD0 and c <= 0xFDEF:
        return False
    if ((c & 0xFFFF) == 0xFFFF) or ((c & 0xFFFF) == 0xFFFE):
        return False
    # control codes
    if c >= 0x00 and c <= 0x08:
        return False
    if c == 0x0B:
        return False
    if c >= 0x0E and c <= 0x1F:
        return False
    if c >= 0x7F and c <= 0x9F:
        return False
    # out of range
    return not (c > 0x10FFFF)

