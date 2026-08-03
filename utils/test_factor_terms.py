from typing import Tuple

def test_factor_terms():
    # issue 7067
    assert factor_list(x*(x + y)) == (1, [(x, 1), (x + y, 1)])
    assert sqf_list(x*(x + y)) == (1, [(x**2 + x*y, 1)])


def test_factor_terms():
    A = Symbol('A', commutative=False)
    assert factor_terms(9*(x + x*y + 1) + (3*x + 3)**(2 + 2*x)) == \
        9*x*y + 9*x + _keep_coeff(S(3), x + 1)**_keep_coeff(S(2), x + 1) + 9
    assert factor_terms(9*(x + x*y + 1) + (3)**(2 + 2*x)) == \
        _keep_coeff(S(9), 3**(2*x) + x*y + x + 1)
    assert factor_terms(3**(2 + 2*x) + a*3**(2 + 2*x)) == \
        9*3**(2*x)*(a + 1)
    assert factor_terms(x + x*A) == \
        x*(1 + A)
    assert factor_terms(sin(x + x*A)) == \
        sin(x*(1 + A))
    assert factor_terms((3*x + 3)**((2 + 2*x)/3)) == \
        _keep_coeff(S(3), x + 1)**_keep_coeff(Rational(2, 3), x + 1)
    assert factor_terms(x + (x*y + x)**(3*x + 3)) == \
        x + (x*(y + 1))**_keep_coeff(S(3), x + 1)
    assert factor_terms(a*(x + x*y) + b*(x*2 + y*x*2)) == \
        x*(a + 2*b)*(y + 1)
    i = Integral(x, (x, 0, oo))
    assert factor_terms(i) == i

    assert factor_terms(x/2 + y) == x/2 + y
    # fraction doesn't apply to integer denominators
    assert factor_terms(x/2 + y, fraction=True) == x/2 + y
    # clear *does* apply to the integer denominators
    assert factor_terms(x/2 + y, clear=True) == Mul(S.Half, x + 2*y, evaluate=False)

    # check radical extraction
    eq = sqrt(2) + sqrt(10)
    assert factor_terms(eq) == eq
    assert factor_terms(eq, radical=True) == sqrt(2)*(1 + sqrt(5))
    eq = root(-6, 3) + root(6, 3)
    assert factor_terms(eq, radical=True) == 6**(S.One/3)*(1 + (-1)**(S.One/3))

    eq = [x + x*y]
    ans = [x*(y + 1)]
    for c in [list, tuple, set]:
        assert factor_terms(c(eq)) == c(ans)
    assert factor_terms(Tuple(x + x*y)) == Tuple(x*(y + 1))
    assert factor_terms(Interval(0, 1)) == Interval(0, 1)
    e = 1/sqrt(a/2 + 1)
    assert factor_terms(e, clear=False) == 1/sqrt(a/2 + 1)
    assert factor_terms(e, clear=True) == sqrt(2)/sqrt(a + 2)

    eq = x/(x + 1/x) + 1/(x**2 + 1)
    assert factor_terms(eq, fraction=False) == eq
    assert factor_terms(eq, fraction=True) == 1

    assert factor_terms((1/(x**3 + x**2) + 2/x**2)*y) == \
        y*(2 + 1/(x + 1))/x**2

    # if not True, then processesing for this in factor_terms is not necessary
    assert gcd_terms(-x - y) == -x - y
    assert factor_terms(-x - y) == Mul(-1, x + y, evaluate=False)

    # if not True, then "special" processesing in factor_terms is not necessary
    assert gcd_terms(exp(Mul(-1, x + 1))) == exp(-x - 1)
    e = exp(-x - 2) + x
    assert factor_terms(e) == exp(Mul(-1, x + 2, evaluate=False)) + x
    assert factor_terms(e, sign=False) == e
    assert factor_terms(exp(-4*x - 2) - x) == -x + exp(Mul(-2, 2*x + 1, evaluate=False))

    # sum/integral tests
    for F in (Sum, Integral):
        assert factor_terms(F(x, (y, 1, 10))) == x * F(1, (y, 1, 10))
        assert factor_terms(F(x, (y, 1, 10)) + x) == x * (1 + F(1, (y, 1, 10)))
        assert factor_terms(F(x*y + x*y**2, (y, 1, 10))) == x*F(y*(y + 1), (y, 1, 10))

    # expressions involving Pow terms with base 0
    assert factor_terms(0**(x - 2) - 1) == 0**(x - 2) - 1
    assert factor_terms(0**(x + 2) - 1) == 0**(x + 2) - 1
    assert factor_terms((0**(x + 2) - 1).subs(x,-2)) == 0

