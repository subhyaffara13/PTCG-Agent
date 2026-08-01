
def test_experimental_lambify():
    x = Symbol('x')
    f = experimental_lambdify([x], Max(x, 5))
    # XXX should f be tested? If f(2) is attempted, an
    # error is raised because a complex produced during wrapping of the arg
    # is being compared with an int.
    assert Max(2, 5) == 5
    assert Max(5, 7) == 7

    x = Symbol('x-3')
    f = experimental_lambdify([x], x + 1)
    assert f(1) == 2

