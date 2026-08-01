
def test_Derivative__new__():
    raises(TypeError, lambda: f(x).diff((x, 2), 0))
    assert f(x, y).diff([(x, y), 0]) == f(x, y)
    assert f(x, y).diff([(x, y), 1]) == NDimArray([
        Derivative(f(x, y), x), Derivative(f(x, y), y)])
    assert f(x,y).diff(y, (x, z), y, x) == Derivative(
        f(x, y), (x, z + 1), (y, 2))
    assert Matrix([x]).diff(x, 2) == Matrix([0])  # is_zero exit

