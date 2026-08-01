
def _wrap_radians(x, *, xp):
    # Wrap radians to (-pi, pi] interval
    wrapped = -((-x + xp.pi) % (2 * xp.pi) - xp.pi)
    # preserve relative precision
    no_wrap = xp.abs(x) < xp.pi
    return xp.where(no_wrap, x, wrapped)

