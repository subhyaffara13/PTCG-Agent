
def test_exp_subs():
    x = Symbol('x')
    e = (exp(3*log(x), evaluate=False))  # evaluates to x**3
    assert e.subs(x**3, y**3) == e
    assert e.subs(x**2, 5) == e
    assert (x**3).subs(x**2, y) != y**Rational(3, 2)
    assert exp(exp(x) + exp(x**2)).subs(exp(exp(x)), y) == y * exp(exp(x**2))
    assert exp(x).subs(E, y) == y**x
    x = symbols('x', real=True)
    assert exp(5*x).subs(exp(7*x), y) == y**Rational(5, 7)
    assert exp(2*x + 7).subs(exp(3*x), y) == y**Rational(2, 3) * exp(7)
    x = symbols('x', positive=True)
    assert exp(3*log(x)).subs(x**2, y) == y**Rational(3, 2)
    # differentiate between E and exp
    assert exp(exp(x + E)).subs(exp, 3) == 3**(3**(x + E))
    assert exp(exp(x + E)).subs(exp, sin) == sin(sin(x + E))
    assert exp(exp(x + E)).subs(E, 3) == 3**(3**(x + 3))
    assert exp(3).subs(E, sin) == sin(3)

