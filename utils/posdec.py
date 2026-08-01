
def posdec(x: int) -> int:
    if x > 0:
        return x - 1
    return x


def posdec(x):
    if x > 0:
        yield x - 1
    else:
        yield x


def posdec(x):
    if isinstance(x, Integer) and x > 0:
        yield x - 1
    else:
        yield x

