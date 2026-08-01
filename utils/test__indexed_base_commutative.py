
def test_IndexedBase_commutative():
    t = IndexedBase('t', commutative=False)
    u = IndexedBase('u', commutative=False)
    v = IndexedBase('v')
    assert t[0]*v[0] == v[0]*t[0]
    assert t[0]*u[0] != u[0]*t[0]

