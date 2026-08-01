
def test_multivar_2():
    assert Order(x**2*y + y**2*x, x, y).expr == x**2*y + y**2*x

