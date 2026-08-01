
def test_scalar_funcs():
    assert SetExpr(Interval(0, 1)).set == Interval(0, 1)
    a, b = Symbol('a', real=True), Symbol('b', real=True)
    a, b = 1, 2
    # TODO: add support for more functions in the future:
    for f in [exp, log]:
        input_se = f(SetExpr(Interval(a, b)))
        output = input_se.set
        expected = Interval(Min(f(a), f(b)), Max(f(a), f(b)))
        assert output == expected

