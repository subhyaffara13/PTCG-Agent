
def test_R2():
    m, b = symbols('m b')
    i, n = symbols('i n', integer=True, positive=True)
    xn = MatrixSymbol('xn', n, 1)
    yn = MatrixSymbol('yn', n, 1)
    f = Sum((yn[i, 0] - m*xn[i, 0] - b)**2, (i, 0, n - 1))
    f1 = diff(f, m)
    f2 = diff(f, b)
    # raises TypeError: solveset() takes at most 2 arguments (3 given)
    solveset((f1, f2), (m, b), domain=S.Reals)


def test_R2():
    x0, y0, r0, theta0 = symbols('x0, y0, r0, theta0', real=True)
    point_r = R2_r.point([x0, y0])
    point_p = R2_p.point([r0, theta0])

    # r**2 = x**2 + y**2
    assert (R2.r**2 - R2.x**2 - R2.y**2).rcall(point_r) == 0
    assert trigsimp( (R2.r**2 - R2.x**2 - R2.y**2).rcall(point_p) ) == 0
    assert trigsimp(R2.e_r(R2.x**2 + R2.y**2).rcall(point_p).doit()) == 2*r0

    # polar->rect->polar == Id
    a, b = symbols('a b', positive=True)
    m = Matrix([[a], [b]])

    #TODO assert m == R2_r.transform(R2_p, R2_p.transform(R2_r, [a, b])).applyfunc(simplify)
    assert m == R2_p.transform(R2_r, R2_r.transform(R2_p, m)).applyfunc(simplify)

    # deprecated method
    with warns_deprecated_sympy():
        assert m == R2_p.coord_tuple_transform_to(
            R2_r, R2_r.coord_tuple_transform_to(R2_p, m)).applyfunc(simplify)

