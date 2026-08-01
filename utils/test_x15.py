
def test_X15():
    # => 0!/x - 1!/x^2 + 2!/x^3 - 3!/x^4 + O(1/x^5)   [Knopp, p. 544]
    x, t = symbols('x t', real=True)
    # raises RuntimeError: maximum recursion depth exceeded
    # https://github.com/sympy/sympy/issues/7164
    # 2019-02-17: Raises
    # PoleError:
    # Asymptotic expansion of Ei around [-oo] is not implemented.
    e1 = integrate(exp(-t)/t, (t, x, oo))
    assert (series(e1, x, x0=oo, n=5) ==
            6/x**4 + 2/x**3 - 1/x**2 + 1/x + O(x**(-5), (x, oo)))

