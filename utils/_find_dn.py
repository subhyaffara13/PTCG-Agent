
def _find_DN(var, coeff):

    x, y = var
    X, Y = symbols("X, Y", integer=True)
    A, B = _transformation_to_DN(var, coeff)

    u = (A*Matrix([X, Y]) + B)[0]
    v = (A*Matrix([X, Y]) + B)[1]
    eq = x**2*coeff[x**2] + x*y*coeff[x*y] + y**2*coeff[y**2] + x*coeff[x] + y*coeff[y] + coeff[1]

    simplified = _mexpand(eq.subs(zip((x, y), (u, v))))

    coeff = simplified.as_coefficients_dict()

    return -coeff[Y**2]/coeff[X**2], -coeff[1]/coeff[X**2]

