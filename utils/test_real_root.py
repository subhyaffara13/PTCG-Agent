
def test_real_root():
    assert real_root(-8, 3) == -2
    assert real_root(-16, 4) == root(-16, 4)
    r = root(-7, 4)
    assert real_root(r) == r
    r1 = root(-1, 3)
    r2 = r1**2
    r3 = root(-1, 4)
    assert real_root(r1 + r2 + r3) == -1 + r2 + r3
    assert real_root(root(-2, 3)) == -root(2, 3)
    assert real_root(-8., 3) == -2.0
    x = Symbol('x')
    n = Symbol('n')
    g = real_root(x, n)
    assert g.subs({"x": -8, "n": 3}) == -2
    assert g.subs({"x": 8, "n": 3}) == 2
    # give principle root if there is no real root -- if this is not desired
    # then maybe a Root class is needed to raise an error instead
    assert g.subs({"x": I, "n": 3}) == cbrt(I)
    assert g.subs({"x": -8, "n": 2}) == sqrt(-8)
    assert g.subs({"x": I, "n": 2}) == sqrt(I)

