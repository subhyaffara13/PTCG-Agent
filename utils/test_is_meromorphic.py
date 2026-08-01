
def test_is_meromorphic():
    f = a/x**2 + b + x + c*x**2
    assert f.is_meromorphic(x, 0) is True
    assert f.is_meromorphic(x, 1) is True
    assert f.is_meromorphic(x, zoo) is True

    g = 3 + 2*x**(log(3)/log(2) - 1)
    assert g.is_meromorphic(x, 0) is False
    assert g.is_meromorphic(x, 1) is True
    assert g.is_meromorphic(x, zoo) is False

    n = Symbol('n', integer=True)
    e = sin(1/x)**n*x
    assert e.is_meromorphic(x, 0) is False
    assert e.is_meromorphic(x, 1) is True
    assert e.is_meromorphic(x, zoo) is False

    e = log(x)**pi
    assert e.is_meromorphic(x, 0) is False
    assert e.is_meromorphic(x, 1) is False
    assert e.is_meromorphic(x, 2) is True
    assert e.is_meromorphic(x, zoo) is False

    assert (log(x)**a).is_meromorphic(x, 0) is False
    assert (log(x)**a).is_meromorphic(x, 1) is False
    assert (a**log(x)).is_meromorphic(x, 0) is None
    assert (3**log(x)).is_meromorphic(x, 0) is False
    assert (3**log(x)).is_meromorphic(x, 1) is True

