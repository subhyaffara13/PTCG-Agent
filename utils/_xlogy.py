
def _xlogy(xp, spsx):
    def __xlogy(x, y, *, xp=xp):
        x, y = xp_promote(x, y, force_floating=True, xp=xp)
        with np.errstate(divide='ignore', invalid='ignore'):
            temp = x * xp.log(y)
        return xp.where(x == 0., 0., temp)
    return __xlogy

