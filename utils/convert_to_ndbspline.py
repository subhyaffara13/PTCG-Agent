
def convert_to_ndbspline(lut):
    tx, ty = lut.get_knots()
    kx, ky = lut.degrees
    nx, ny = len(tx), len(ty)
    c = lut.get_coeffs().reshape((nx - kx - 1, ny - ky - 1))
    return NdBSpline((tx, ty), c, (kx, ky))

