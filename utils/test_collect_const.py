
def test_collect_const():
    # coverage not provided by above tests
    assert collect_const(2*sqrt(3) + 4*a*sqrt(5)) == \
        2*(2*sqrt(5)*a + sqrt(3))  # let the primitive reabsorb
    assert collect_const(2*sqrt(3) + 4*a*sqrt(5), sqrt(3)) == \
        2*sqrt(3) + 4*a*sqrt(5)
    assert collect_const(sqrt(2)*(1 + sqrt(2)) + sqrt(3) + x*sqrt(2)) == \
        sqrt(2)*(x + 1 + sqrt(2)) + sqrt(3)

    # issue 5290
    assert collect_const(2*x + 2*y + 1, 2) == \
        collect_const(2*x + 2*y + 1) == \
        Add(S.One, Mul(2, x + y, evaluate=False), evaluate=False)
    assert collect_const(-y - z) == Mul(-1, y + z, evaluate=False)
    assert collect_const(2*x - 2*y - 2*z, 2) == \
        Mul(2, x - y - z, evaluate=False)
    assert collect_const(2*x - 2*y - 2*z, -2) == \
        _unevaluated_Add(2*x, Mul(-2, y + z, evaluate=False))

    # this is why the content_primitive is used
    eq = (sqrt(15 + 5*sqrt(2))*x + sqrt(3 + sqrt(2))*y)*2
    assert collect_sqrt(eq + 2) == \
        2*sqrt(sqrt(2) + 3)*(sqrt(5)*x + y) + 2

    # issue 16296
    assert collect_const(a + b + x/2 + y/2) == a + b + Mul(S.Half, x + y, evaluate=False)

