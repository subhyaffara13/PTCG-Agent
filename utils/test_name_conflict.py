
def test_name_conflict():
    z1 = x0 + y
    z2 = x2 + x3
    l = [cos(z1) + z1, cos(z2) + z2, x0 + x2]
    substs, reduced = cse(l)
    assert [e.subs(reversed(substs)) for e in reduced] == l

