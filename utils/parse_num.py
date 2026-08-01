
def parse_num(maybe_num: str) -> int:
    """Parse number path suffixes, returns -1 on error."""
    try:
        return int(maybe_num)
    except ValueError:
        return -1


def parseNum(s):
    try:
        value = int(s)
    except:
        value = float(s)
    return value

