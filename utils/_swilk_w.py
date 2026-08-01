
def _swilk_w(y, a, *, xp):
    # calculate Shapiro-Wilk statistic given sorted sample and weights
    # Follows [4] Section 2.1
    num = xp.vecdot(a, y, axis=-1) ** 2
    y_ = _demean(y, mean=xp.mean(y, axis=-1, keepdims=True), axis=-1, xp=xp)
    den = xp.vecdot(y_, y_, axis=-1)
    return num / den

