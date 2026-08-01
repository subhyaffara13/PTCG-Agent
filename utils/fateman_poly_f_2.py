
def fateman_poly_F_2(n):
    """Fateman's GCD benchmark: linearly dense quartic inputs """
    Y = [Symbol('y_' + str(i)) for i in range(n + 1)]

    y_0 = Y[0]

    u = Add(*Y[1:])

    H = Poly((y_0 + u + 1)**2, *Y)

    F = Poly((y_0 - u - 2)**2, *Y)
    G = Poly((y_0 + u + 2)**2, *Y)

    return H*F, H*G, H

