
def test_basics_multiple():
    assert diff_test(Integral(x, (x, 3*x, 5*y), (y, x, 2*x))) == {x}
    assert diff_test(Integral(x, (x, 5*y), (y, x, 2*x))) == {x}
    assert diff_test(Integral(x, (x, 5*y), (y, y, 2*x))) == {x, y}
    assert diff_test(Integral(y, y, x)) == {x, y}
    assert diff_test(Integral(y*x, x, y)) == {x, y}
    assert diff_test(Integral(x + y, y, (y, 1, x))) == {x}
    assert diff_test(Integral(x + y, (x, x, y), (y, y, x))) == {x, y}

