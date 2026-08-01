
def test_dict_set():
    a, b, c = map(Wild, 'abc')

    f = 3*cos(4*x)
    r = f.match(a*cos(b*x))
    assert r == {a: 3, b: 4}
    e = a/b*sin(b*x)
    assert e.subs(r) == r[a]/r[b]*sin(r[b]*x)
    assert e.subs(r) == 3*sin(4*x) / 4
    s = set(r.items())
    assert e.subs(s) == r[a]/r[b]*sin(r[b]*x)
    assert e.subs(s) == 3*sin(4*x) / 4

    assert e.subs(r) == r[a]/r[b]*sin(r[b]*x)
    assert e.subs(r) == 3*sin(4*x) / 4
    assert x.subs(Dict((x, 1))) == 1

