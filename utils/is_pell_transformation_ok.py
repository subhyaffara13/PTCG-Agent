
def is_pell_transformation_ok(eq):
    """
    Test whether X*Y, X, or Y terms are present in the equation
    after transforming the equation using the transformation returned
    by transformation_to_pell(). If they are not present we are good.
    Moreover, coefficient of X**2 should be a divisor of coefficient of
    Y**2 and the constant term.
    """
    A, B = transformation_to_DN(eq)
    u = (A*Matrix([X, Y]) + B)[0]
    v = (A*Matrix([X, Y]) + B)[1]
    simplified = diop_simplify(eq.subs(zip((x, y), (u, v))))

    coeff = dict([reversed(t.as_independent(*[X, Y])) for t in simplified.args])

    for term in [X*Y, X, Y]:
        if term in coeff.keys():
            return False

    for term in [X**2, Y**2, 1]:
        if term not in coeff.keys():
            coeff[term] = 0

    if coeff[X**2] != 0:
        return divisible(coeff[Y**2], coeff[X**2]) and \
        divisible(coeff[1], coeff[X**2])

    return True

