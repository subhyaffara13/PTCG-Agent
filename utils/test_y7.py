
def test_Y7():
    # What is the Laplace transform of an infinite square wave?
    # => 1/s + 2 sum( (-1)^n e^(- s n a)/s, n = 1..infinity )
    #    [Sanchez, Allen and Kyner, p. 213]
    t = symbols('t', positive=True)
    a = symbols('a', real=True)
    s = symbols('s')
    F, _, _ = laplace_transform(1 + 2*Sum((-1)**n*Heaviside(t - n*a),
                                          (n, 1, oo)), t, s)
    # returns 2*LaplaceTransform(Sum((-1)**n*Heaviside(-a*n + t),
    #                                (n, 1, oo)), t, s) + 1/s
    # https://github.com/sympy/sympy/issues/7177
    assert F == 2*Sum((-1)**n*exp(-a*n*s)/s, (n, 1, oo)) + 1/s

