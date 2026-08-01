
def test_derivative_subs_self_bug():
    d = diff(f(x), x)

    assert d.subs(d, y) == y

