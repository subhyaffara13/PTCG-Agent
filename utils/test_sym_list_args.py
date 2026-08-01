
def test_sym_list_args():
    f = lambdify([x, y], x + y + z)
    assert f(1, 2) == 3 + z

