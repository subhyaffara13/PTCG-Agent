
def test_IndexedBase_subs():
    i = symbols('i', integer=True)
    a, b = symbols('a b')
    A = IndexedBase(a)
    B = IndexedBase(b)
    assert A[i] == B[i].subs(b, a)
    C = {1: 2}
    assert C[1] == A[1].subs(A, C)

