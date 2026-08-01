
def test_no_args():
    f = lambdify([], 1)
    raises(TypeError, lambda: f(-1))
    assert f() == 1

