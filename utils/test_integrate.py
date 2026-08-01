
def test_integrate():
    x, y = symbols('x y')
    m = CalculusOnlyMatrix(2, 1, [x, y])
    assert m.integrate(x) == Matrix(2, 1, [x**2/2, y*x])


def test_integrate():
    intIM = integrate(IM, x)
    assert intIM.shape == IM.shape
    assert all(intIM[i, j] == (1 + j + 3*i)*x for i, j in
                product(range(3), range(3)))


def test_integrate():
    A = Matrix(((1, 4, x), (y, 2, 4), (10, 5, x**2)))
    assert A.integrate(x) == \
        Matrix(((x, 4*x, x**2/2), (x*y, 2*x, 4*x), (10*x, 5*x, x**3/3)))
    assert A.integrate(y) == \
        Matrix(((y, 4*y, x*y), (y**2/2, 2*y, 4*y), (10*y, 5*y, y*x**2)))


def test_integrate():
    A = Matrix(((1, 4, x), (y, 2, 4), (10, 5, x**2)))
    assert A.integrate(x) == \
        Matrix(((x, 4*x, x**2/2), (x*y, 2*x, 4*x), (10*x, 5*x, x**3/3)))
    assert A.integrate(y) == \
        Matrix(((y, 4*y, x*y), (y**2/2, 2*y, 4*y), (10*y, 5*y, y*x**2)))
    m = Matrix(2, 1, [x, y])
    assert m.integrate(x) == Matrix(2, 1, [x**2/2, y*x])


def test_integrate():
    x = symbols('x')
    R, Dx = DifferentialOperators(ZZ.old_poly_ring(x), 'Dx')
    p = expr_to_holonomic(sin(x)**2/x, x0=1).integrate((x, 2, 3))
    q = '0.166270406994788'
    assert sstr(p) == q
    p = expr_to_holonomic(sin(x)).integrate((x, 0, x)).to_expr()
    q = 1 - cos(x)
    assert p == q
    p = expr_to_holonomic(sin(x)).integrate((x, 0, 3))
    q = 1 - cos(3)
    assert p == q
    p = expr_to_holonomic(sin(x)/x, x0=1).integrate((x, 1, 2))
    q = '0.659329913368450'
    assert sstr(p) == q
    p = expr_to_holonomic(sin(x)**2/x, x0=1).integrate((x, 1, 0))
    q = '-0.423690480850035'
    assert sstr(p) == q
    p = expr_to_holonomic(sin(x)/x)
    assert p.integrate(x).to_expr() == Si(x)
    assert p.integrate((x, 0, 2)) == Si(2)
    p = expr_to_holonomic(sin(x)**2/x)
    q = p.to_expr()
    assert p.integrate(x).to_expr() == q.integrate((x, 0, x))
    assert p.integrate((x, 0, 1)) == q.integrate((x, 0, 1))
    assert expr_to_holonomic(1/x, x0=1).integrate(x).to_expr() == log(x)
    p = expr_to_holonomic((x + 1)**3*exp(-x), x0=-1).integrate(x).to_expr()
    q = (-x**3 - 6*x**2 - 15*x + 6*exp(x + 1) - 16)*exp(-x)
    assert p == q
    p = expr_to_holonomic(cos(x)**2/x**2, y0={-2: [1, 0, -1]}).integrate(x).to_expr()
    q = -Si(2*x) - cos(x)**2/x
    assert p == q
    p = expr_to_holonomic(sqrt(x**2+x)).integrate(x).to_expr()
    q = (x**Rational(3, 2)*(2*x**2 + 3*x + 1) - x*sqrt(x + 1)*asinh(sqrt(x)))/(4*x*sqrt(x + 1))
    assert p == q
    p = expr_to_holonomic(sqrt(x**2+1)).integrate(x).to_expr()
    q = (sqrt(x**2+1)).integrate(x)
    assert (p-q).simplify() == 0
    p = expr_to_holonomic(1/x**2, y0={-2:[1, 0, 0]})
    r = expr_to_holonomic(1/x**2, lenics=3)
    assert p == r
    q = expr_to_holonomic(cos(x)**2)
    assert (r*q).integrate(x).to_expr() == -Si(2*x) - cos(x)**2/x


def test_integrate():
    assert x.integrate(x) == x**2/2
    assert x.integrate((x, 0, 1)) == S.Half

