
def test_Complement_as_relational_fail():
    x = Symbol('x')
    expr = Complement(Interval(0, 1), FiniteSet(2), evaluate=False)
    # XXX This example fails because 0 <= x changes to x >= 0
    # during the evaluation.
    assert expr.as_relational(x) == \
            (0 <= x) & (x <= 1) & Ne(x, 2)

