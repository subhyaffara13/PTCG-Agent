
def _transformation_to_DN(var, coeff):

    x, y = var

    a = coeff[x**2]
    b = coeff[x*y]
    c = coeff[y**2]
    d = coeff[x]
    e = coeff[y]
    f = coeff[1]

    a, b, c, d, e, f = [as_int(i) for i in _remove_gcd(a, b, c, d, e, f)]

    X, Y = symbols("X, Y", integer=True)

    if b:
        B, C = _rational_pq(2*a, b)
        A, T = _rational_pq(a, B**2)

        # eq_1 = A*B*X**2 + B*(c*T - A*C**2)*Y**2 + d*T*X + (B*e*T - d*T*C)*Y + f*T*B
        coeff = {X**2: A*B, X*Y: 0, Y**2: B*(c*T - A*C**2), X: d*T, Y: B*e*T - d*T*C, 1: f*T*B}
        A_0, B_0 = _transformation_to_DN([X, Y], coeff)
        return Matrix(2, 2, [S.One/B, -S(C)/B, 0, 1])*A_0, Matrix(2, 2, [S.One/B, -S(C)/B, 0, 1])*B_0

    if d:
        B, C = _rational_pq(2*a, d)
        A, T = _rational_pq(a, B**2)

        # eq_2 = A*X**2 + c*T*Y**2 + e*T*Y + f*T - A*C**2
        coeff = {X**2: A, X*Y: 0, Y**2: c*T, X: 0, Y: e*T, 1: f*T - A*C**2}
        A_0, B_0 = _transformation_to_DN([X, Y], coeff)
        return Matrix(2, 2, [S.One/B, 0, 0, 1])*A_0, Matrix(2, 2, [S.One/B, 0, 0, 1])*B_0 + Matrix([-S(C)/B, 0])

    if e:
        B, C = _rational_pq(2*c, e)
        A, T = _rational_pq(c, B**2)

        # eq_3 = a*T*X**2 + A*Y**2 + f*T - A*C**2
        coeff = {X**2: a*T, X*Y: 0, Y**2: A, X: 0, Y: 0, 1: f*T - A*C**2}
        A_0, B_0 = _transformation_to_DN([X, Y], coeff)
        return Matrix(2, 2, [1, 0, 0, S.One/B])*A_0, Matrix(2, 2, [1, 0, 0, S.One/B])*B_0 + Matrix([0, -S(C)/B])

    # TODO: pre-simplification: Not necessary but may simplify
    # the equation.
    return Matrix(2, 2, [S.One/a, 0, 0, 1]), Matrix([0, 0])

