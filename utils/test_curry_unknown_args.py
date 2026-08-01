
def test_curry_unknown_args():
    def add3(x, y, z):
        return x + y + z

    @curry
    def f(*args):
        return add3(*args)

    assert f()(1)(2)(3) == 6
    assert f(1)(2)(3) == 6
    assert f(1, 2)(3) == 6
    assert f(1, 2, 3) == 6
    assert f(1, 2)(3, 4) == f(1, 2, 3, 4)

