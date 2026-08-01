
def thin_plate_spline(r, xp):
    # NB: changed w.r.t. pythran, vectorized
    return xp.where(r == 0, 0, r**2 * xp.log(r))

