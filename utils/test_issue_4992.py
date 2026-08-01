
def test_issue_4992():
    # Nonelementary integral.  Requires hypergeometric/Meijer-G handling.
    assert not integrate(log(x) * x**(k - 1) * exp(-x) / gamma(k), (x, 0, oo)).has(Integral)


def test_issue_4992():
    # Note: psi in _check_antecedents becomes NaN.
    from sympy.core.function import expand_func
    a = Symbol('a', positive=True)
    assert simplify(expand_func(integrate(exp(-x)*log(x)*x**a, (x, 0, oo)))) == \
        (a*polygamma(0, a) + 1)*gamma(a)

