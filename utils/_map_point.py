
def _map_point(matrix, pt):
    # apply Transform matrix to a point represented as a complex number
    r = matrix.transformPoint((pt.real, pt.imag))
    return r[0] + r[1] * 1j

