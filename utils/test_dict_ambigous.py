
def test_dict_ambigous():   # see issue 3566
    f = x*exp(x)
    g = z*exp(z)

    df = {x: y, exp(x): y}
    dg = {z: y, exp(z): y}

    assert f.subs(df) == y**2
    assert g.subs(dg) == y**2

    # and this is how order can affect the result
    assert f.subs(x, y).subs(exp(x), y) == y*exp(y)
    assert f.subs(exp(x), y).subs(x, y) == y**2

    # length of args and count_ops are the same so
    # default_sort_key resolves ordering...if one
    # doesn't want this result then an unordered
    # sequence should not be used.
    e = 1 + x*y
    assert e.subs({x: y, y: 2}) == 5
    # here, there are no obviously clashing keys or values
    # but the results depend on the order
    assert exp(x/2 + y).subs({exp(y + 1): 2, x: 2}) == exp(y + 1)

