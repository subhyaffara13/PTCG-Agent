
def test_vector_simplify():
    A, s, k, m = symbols('A, s, k, m')

    test1 = (1 / a + 1 / b) * i
    assert (test1 & i) != (a + b) / (a * b)
    test1 = simplify(test1)
    assert (test1 & i) == (a + b) / (a * b)
    assert test1.simplify() == simplify(test1)

    test2 = (A**2 * s**4 / (4 * pi * k * m**3)) * i
    test2 = simplify(test2)
    assert (test2 & i) == (A**2 * s**4 / (4 * pi * k * m**3))

    test3 = ((4 + 4 * a - 2 * (2 + 2 * a)) / (2 + 2 * a)) * i
    test3 = simplify(test3)
    assert (test3 & i) == 0

    test4 = ((-4 * a * b**2 - 2 * b**3 - 2 * a**2 * b) / (a + b)**2) * i
    test4 = simplify(test4)
    assert (test4 & i) == -2 * b

    v = (sin(a)+cos(a))**2*i - j
    assert trigsimp(v) == (2*sin(a + pi/4)**2)*i + (-1)*j
    assert trigsimp(v) == v.trigsimp()

    assert simplify(Vector.zero) == Vector.zero


def test_vector_simplify():
    x, y, z, k, n, m, w, f, s, A = symbols('x, y, z, k, n, m, w, f, s, A')
    N = ReferenceFrame('N')

    test1 = (1 / x + 1 / y) * N.x
    assert (test1 & N.x) != (x + y) / (x * y)
    test1 = test1.simplify()
    assert (test1 & N.x) == (x + y) / (x * y)

    test2 = (A**2 * s**4 / (4 * pi * k * m**3)) * N.x
    test2 = test2.simplify()
    assert (test2 & N.x) == (A**2 * s**4 / (4 * pi * k * m**3))

    test3 = ((4 + 4 * x - 2 * (2 + 2 * x)) / (2 + 2 * x)) * N.x
    test3 = test3.simplify()
    assert (test3 & N.x) == 0

    test4 = ((-4 * x * y**2 - 2 * y**3 - 2 * x**2 * y) / (x + y)**2) * N.x
    test4 = test4.simplify()
    assert (test4 & N.x) == -2 * y

