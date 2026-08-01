
def test_indexed_idx_sum():
    i = symbols('i', cls=Idx)
    r = Indexed('r', i)
    assert Sum(r, (i, 0, 3)).doit() == sum(r.xreplace({i: j}) for j in range(4))
    assert Product(r, (i, 0, 3)).doit() == prod([r.xreplace({i: j}) for j in range(4)])

    j = symbols('j', integer=True)
    assert Sum(r, (i, j, j+2)).doit() == sum(r.xreplace({i: j+k}) for k in range(3))
    assert Product(r, (i, j, j+2)).doit() == prod([r.xreplace({i: j+k}) for k in range(3)])

    k = Idx('k', range=(1, 3))
    A = IndexedBase('A')
    assert Sum(A[k], k).doit() == sum(A[Idx(j, (1, 3))] for j in range(1, 4))
    assert Product(A[k], k).doit() == prod([A[Idx(j, (1, 3))] for j in range(1, 4)])

    raises(ValueError, lambda: Sum(A[k], (k, 1, 4)))
    raises(ValueError, lambda: Sum(A[k], (k, 0, 3)))
    raises(ValueError, lambda: Sum(A[k], (k, 2, oo)))

    raises(ValueError, lambda: Product(A[k], (k, 1, 4)))
    raises(ValueError, lambda: Product(A[k], (k, 0, 3)))
    raises(ValueError, lambda: Product(A[k], (k, 2, oo)))

