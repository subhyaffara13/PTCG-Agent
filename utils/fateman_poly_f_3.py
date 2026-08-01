
def fateman_poly_F_3(n):
    """Fateman's GCD benchmark: sparse inputs (deg f ~ vars f) """
    Y = [Symbol('y_' + str(i)) for i in range(n + 1)]

    y_0 = Y[0]

    u = Add(*[y**(n + 1) for y in Y[1:]])

    H = Poly((y_0**(n + 1) + u + 1)**2, *Y)

    F = Poly((y_0**(n + 1) - u - 2)**2, *Y)
    G = Poly((y_0**(n + 1) + u + 2)**2, *Y)

    return H*F, H*G, H

