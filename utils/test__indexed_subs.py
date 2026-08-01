
def test_Indexed_subs():
    i, j, k = symbols('i j k', integer=True)
    a, b = symbols('a b')
    A = IndexedBase(a)
    B = IndexedBase(b)
    assert A[i, j] == B[i, j].subs(b, a)
    assert A[i, j] == A[i, k].subs(k, j)

