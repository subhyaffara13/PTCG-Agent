
def test_checksol():
    x, y, r, t = symbols('x, y, r, t')
    eq = r - x**2 - y**2
    dict_var_soln = {y: - sqrt(r) / sqrt(tan(t)**2 + 1),
        x: -sqrt(r)*tan(t)/sqrt(tan(t)**2 + 1)}
    assert checksol(eq, dict_var_soln) == True
    assert checksol(Eq(x, False), {x: False}) is True
    assert checksol(Ne(x, False), {x: False}) is False
    assert checksol(Eq(x < 1, True), {x: 0}) is True
    assert checksol(Eq(x < 1, True), {x: 1}) is False
    assert checksol(Eq(x < 1, False), {x: 1}) is True
    assert checksol(Eq(x < 1, False), {x: 0}) is False
    assert checksol(Eq(x + 1, x**2 + 1), {x: 1}) is True
    assert checksol([x - 1, x**2 - 1], x, 1) is True
    assert checksol([x - 1, x**2 - 2], x, 1) is False
    assert checksol(Poly(x**2 - 1), x, 1) is True
    assert checksol(0, {}) is True
    assert checksol([1e-10, x - 2], x, 2) is False
    assert checksol([0.5, 0, x], x, 0) is False
    assert checksol(y, x, 2) is False
    assert checksol(x+1e-10, x, 0, numerical=True) is True
    assert checksol(x+1e-10, x, 0, numerical=False) is False
    assert checksol(exp(92*x), {x: log(sqrt(2)/2)}) is False
    assert checksol(exp(92*x), {x: log(sqrt(2)/2) + I*pi}) is False
    assert checksol(1/x**5, x, 1000) is False
    raises(ValueError, lambda: checksol(x, 1))
    raises(ValueError, lambda: checksol([], x, 1))

