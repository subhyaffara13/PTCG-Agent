
def test_curry_kwargs():
    def f(a, b, c=10):
        return (a + b) * c

    f = curry(f)
    assert f(1, 2, 3) == 9
    assert f(1)(2, 3) == 9
    assert f(1, 2) == 30
    assert f(1, c=3)(2) == 9
    assert f(c=3)(1, 2) == 9

    def g(a=1, b=10, c=0):
        return a + b + c

    cg = curry(g, b=2)
    assert cg() == 3
    assert cg(b=3) == 4
    assert cg(a=0) == 2
    assert cg(a=0, b=1) == 1
    assert cg(0) == 2  # pass "a" as arg, not kwarg
    assert raises(TypeError, lambda: cg(1, 2))  # pass "b" as arg AND kwarg

    def h(x, func=int):
        return func(x)

    # __init__ must not pick func as positional arg
    assert curry(h)(0.0) == 0
    assert curry(h)(func=str)(0.0) == '0.0'
    assert curry(h, func=str)(0.0) == '0.0'

