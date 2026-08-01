
def test_IndexedBase_shape():
    i, j, m, n = symbols('i j m n', integer=True)
    a = IndexedBase('a', shape=(m, m))
    b = IndexedBase('a', shape=(m, n))
    assert b.shape == Tuple(m, n)
    assert a[i, j] != b[i, j]
    assert a[i, j] == b[i, j].subs(n, m)
    assert b.func(*b.args) == b
    assert b[i, j].func(*b[i, j].args) == b[i, j]
    raises(IndexException, lambda: b[i])
    raises(IndexException, lambda: b[i, i, j])
    F = IndexedBase("F", shape=m)
    assert F.shape == Tuple(m)
    assert F[i].subs(i, j) == F[j]
    raises(IndexException, lambda: F[i, j])

