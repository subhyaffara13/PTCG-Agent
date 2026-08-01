
def _pre_warp(wp, ws, analog, *, xp):
    # Pre-warp frequencies for digital filter design
    if not analog:
        passb = xp.tan(xp.pi * wp / 2.0)
        stopb = xp.tan(xp.pi * ws / 2.0)
    else:
        passb, stopb = wp, ws
    return passb, stopb

