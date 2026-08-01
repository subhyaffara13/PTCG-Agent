
def test_lambdify_dummy_arg():
    d1 = Dummy()
    f1 = lambdify(d1, d1 + 1, dummify=False)
    assert f1(2) == 3
    f1b = lambdify(d1, d1 + 1)
    assert f1b(2) == 3
    d2 = Dummy('x')
    f2 = lambdify(d2, d2 + 1)
    assert f2(2) == 3
    f3 = lambdify([[d2]], d2 + 1)
    assert f3([2]) == 3

