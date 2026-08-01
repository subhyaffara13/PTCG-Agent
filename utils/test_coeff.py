
def test_coeff():
    assert (x + 1).coeff(x + 1) == 1
    assert (3*x).coeff(0) == 0
    assert (z*(1 + x)*x**2).coeff(1 + x) == z*x**2
    assert (1 + 2*x*x**(1 + x)).coeff(x*x**(1 + x)) == 2
    assert (1 + 2*x**(y + z)).coeff(x**(y + z)) == 2
    assert (3 + 2*x + 4*x**2).coeff(1) == 0
    assert (3 + 2*x + 4*x**2).coeff(-1) == 0
    assert (3 + 2*x + 4*x**2).coeff(x) == 2
    assert (3 + 2*x + 4*x**2).coeff(x**2) == 4
    assert (3 + 2*x + 4*x**2).coeff(x**3) == 0

    assert (-x/8 + x*y).coeff(x) == Rational(-1, 8) + y
    assert (-x/8 + x*y).coeff(-x) == S.One/8
    assert (4*x).coeff(2*x) == 0
    assert (2*x).coeff(2*x) == 1
    assert (-oo*x).coeff(x*oo) == -1
    assert (10*x).coeff(x, 0) == 0
    assert (10*x).coeff(10*x, 0) == 0

    n1, n2 = symbols('n1 n2', commutative=False)
    assert (n1*n2).coeff(n1) == 1
    assert (n1*n2).coeff(n2) == n1
    assert (n1*n2 + x*n1).coeff(n1) == 1  # 1*n1*(n2+x)
    assert (n2*n1 + x*n1).coeff(n1) == n2 + x
    assert (n2*n1 + x*n1**2).coeff(n1) == n2
    assert (n1**x).coeff(n1) == 0
    assert (n1*n2 + n2*n1).coeff(n1) == 0
    assert (2*(n1 + n2)*n2).coeff(n1 + n2, right=1) == n2
    assert (2*(n1 + n2)*n2).coeff(n1 + n2, right=0) == 2

    assert (2*f(x) + 3*f(x).diff(x)).coeff(f(x)) == 2

    expr = z*(x + y)**2
    expr2 = z*(x + y)**2 + z*(2*x + 2*y)**2
    assert expr.coeff(z) == (x + y)**2
    assert expr.coeff(x + y) == 0
    assert expr2.coeff(z) == (x + y)**2 + (2*x + 2*y)**2

    assert (x + y + 3*z).coeff(1) == x + y
    assert (-x + 2*y).coeff(-1) == x
    assert (x - 2*y).coeff(-1) == 2*y
    assert (3 + 2*x + 4*x**2).coeff(1) == 0
    assert (-x - 2*y).coeff(2) == -y
    assert (x + sqrt(2)*x).coeff(sqrt(2)) == x
    assert (3 + 2*x + 4*x**2).coeff(x) == 2
    assert (3 + 2*x + 4*x**2).coeff(x**2) == 4
    assert (3 + 2*x + 4*x**2).coeff(x**3) == 0
    assert (z*(x + y)**2).coeff((x + y)**2) == z
    assert (z*(x + y)**2).coeff(x + y) == 0
    assert (2 + 2*x + (x + 1)*y).coeff(x + 1) == y

    assert (x + 2*y + 3).coeff(1) == x
    assert (x + 2*y + 3).coeff(x, 0) == 2*y + 3
    assert (x**2 + 2*y + 3*x).coeff(x**2, 0) == 2*y + 3*x
    assert x.coeff(0, 0) == 0
    assert x.coeff(x, 0) == 0

    n, m, o, l = symbols('n m o l', commutative=False)
    assert n.coeff(n) == 1
    assert y.coeff(n) == 0
    assert (3*n).coeff(n) == 3
    assert (2 + n).coeff(x*m) == 0
    assert (2*x*n*m).coeff(x) == 2*n*m
    assert (2 + n).coeff(x*m*n + y) == 0
    assert (2*x*n*m).coeff(3*n) == 0
    assert (n*m + m*n*m).coeff(n) == 1 + m
    assert (n*m + m*n*m).coeff(n, right=True) == m  # = (1 + m)*n*m
    assert (n*m + m*n).coeff(n) == 0
    assert (n*m + o*m*n).coeff(m*n) == o
    assert (n*m + o*m*n).coeff(m*n, right=True) == 1
    assert (n*m + n*m*n).coeff(n*m, right=True) == 1 + n  # = n*m*(n + 1)

    assert (x*y).coeff(z, 0) == x*y

    assert (x*n + y*n + z*m).coeff(n) == x + y
    assert (n*m + n*o + o*l).coeff(n, right=True) == m + o
    assert (x*n*m*n + y*n*m*o + z*l).coeff(m, right=True) == x*n + y*o
    assert (x*n*m*n + x*n*m*o + z*l).coeff(m, right=True) == n + o
    assert (x*n*m*n + x*n*m*o + z*l).coeff(m) == x*n

