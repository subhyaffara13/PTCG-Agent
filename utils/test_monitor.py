
def test_monitor():
    f = lambda x: x**2
    a = []
    b = []
    g = monitor(f, a.append, b.append)
    assert g(3) == 9
    assert g(4) == 16
    assert a[0] == ((3,), {})
    assert b[0] == 9

