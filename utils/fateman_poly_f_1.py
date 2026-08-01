
def fateman_poly_F_1(n):
    """Fateman's GCD benchmark: trivial GCD """
    Y = [Symbol('y_' + str(i)) for i in range(n + 1)]

    y_0, y_1 = Y[0], Y[1]

    u = y_0 + Add(*Y[1:])
    v = y_0**2 + Add(*[y**2 for y in Y[1:]])

    F = ((u + 1)*(u + 2)).as_poly(*Y)
    G = ((v + 1)*(-3*y_1*y_0**2 + y_1**2 - 1)).as_poly(*Y)

    H = Poly(1, *Y)

    return F, G, H

