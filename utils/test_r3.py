
def test_R3():
    n, k = symbols('n k', integer=True, positive=True)
    sk = ((-1)**k) * (binomial(2*n, k))**2
    Sm = Sum(sk, (k, 1, oo))
    T = Sm.doit()
    T2 = T.combsimp()
    # returns -((-1)**n*factorial(2*n)
    #           - (factorial(n))**2)*exp_polar(-I*pi)/(factorial(n))**2
    assert T2 == (-1)**n*binomial(2*n, n)


def test_R3():
    a, b, c = symbols('a b c', positive=True)
    m = Matrix([[a], [b], [c]])

    assert m == R3_c.transform(R3_r, R3_r.transform(R3_c, m)).applyfunc(simplify)
    #TODO assert m == R3_r.transform(R3_c, R3_c.transform(R3_r, m)).applyfunc(simplify)
    assert m == R3_s.transform(
        R3_r, R3_r.transform(R3_s, m)).applyfunc(simplify)
    #TODO assert m == R3_r.transform(R3_s, R3_s.transform(R3_r, m)).applyfunc(simplify)
    assert m == R3_s.transform(
        R3_c, R3_c.transform(R3_s, m)).applyfunc(simplify)
    #TODO assert m == R3_c.transform(R3_s, R3_s.transform(R3_c, m)).applyfunc(simplify)

    with warns_deprecated_sympy():
        assert m == R3_c.coord_tuple_transform_to(
            R3_r, R3_r.coord_tuple_transform_to(R3_c, m)).applyfunc(simplify)
        #TODO assert m == R3_r.coord_tuple_transform_to(R3_c, R3_c.coord_tuple_transform_to(R3_r, m)).applyfunc(simplify)
        assert m == R3_s.coord_tuple_transform_to(
            R3_r, R3_r.coord_tuple_transform_to(R3_s, m)).applyfunc(simplify)
        #TODO assert m == R3_r.coord_tuple_transform_to(R3_s, R3_s.coord_tuple_transform_to(R3_r, m)).applyfunc(simplify)
        assert m == R3_s.coord_tuple_transform_to(
            R3_c, R3_c.coord_tuple_transform_to(R3_s, m)).applyfunc(simplify)

