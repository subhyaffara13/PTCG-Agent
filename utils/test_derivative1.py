
def test_derivative1():
    x, y = map(Symbol, 'xy')
    p, q = map(Wild, 'pq')

    f = Function('f', nargs=1)
    fd = Derivative(f(x), x)

    assert fd.match(p) == {p: fd}
    assert (fd + 1).match(p + 1) == {p: fd}
    assert (fd).match(fd) == {}
    assert (3*fd).match(p*fd) is not None
    assert (3*fd - 1).match(p*fd + q) == {p: 3, q: -1}

