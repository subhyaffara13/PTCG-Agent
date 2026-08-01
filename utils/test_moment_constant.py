
def test_moment_constant():
    assert moment(3, 0) == 1
    assert moment(3, 1) == 3
    assert moment(3, 2) == 9
    x = Symbol('x')
    assert moment(x, 2) == x**2

