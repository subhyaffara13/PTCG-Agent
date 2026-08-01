
def test_list_args():
    f = lambdify([x, y], x + y)
    assert f(1, 2) == 3

