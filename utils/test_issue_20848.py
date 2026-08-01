
def test_issue_20848():
    _i = Dummy('i')
    t, y, z = symbols('t y z')
    assert diff(Product(x, (y, 1, z)), x).as_dummy() == Sum(Product(x, (y, 1, _i - 1))*Product(x, (y, _i + 1, z)), (_i, 1, z)).as_dummy()
    assert diff(Product(x, (y, 1, z)), x).doit() == x**(z - 1)*z
    assert diff(Product(x, (y, x, z)), x) == Derivative(Product(x, (y, x, z)), x)
    assert diff(Product(t, (x, 1, z)), x) == S(0)
    assert Product(sin(n*x), (n, -1, 1)).diff(x).doit() == S(0)

