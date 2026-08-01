
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def distance(p1, p2):
    """Trip length between two planets — ceil of Euclidean distance.

    Matches GameDesc::Distance in game.h. Accepts Planet namedtuples, raw
    lists ([id, x, y, ...]), or (x, y) tuples.
    """
    x1, y1 = _xy(p1)
    x2, y2 = _xy(p2)
    return math.ceil(math.hypot(x1 - x2, y1 - y2))

