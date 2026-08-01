
def _denormalize(v, triplet):
    if v >= 0:
        return triplet[1] + v * (triplet[2] - triplet[1])
    else:
        return triplet[1] + v * (triplet[1] - triplet[0])


def _denormalize(v, axis):
    if v >= 0:
        return axis.defaultValue + v * (axis.maxValue - axis.defaultValue)
    else:
        return axis.defaultValue + v * (axis.defaultValue - axis.minValue)

