
def setup_quadratic_to_curves():
    curves = generate_curves(NUM_CURVES)
    quadratics = [curve_to_quadratic(curve, MAX_ERR) for curve in curves]
    return quadratics, MAX_ERR

