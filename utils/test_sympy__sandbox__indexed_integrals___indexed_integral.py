
def test_sympy__sandbox__indexed_integrals__IndexedIntegral():
    from sympy.tensor import IndexedBase, Idx
    from sympy.sandbox.indexed_integrals import IndexedIntegral
    A = IndexedBase('A')
    i, j = symbols('i j', integer=True)
    a1, a2 = symbols('a1:3', cls=Idx)
    assert _test_args(IndexedIntegral(A[a1], A[a2]))
    assert _test_args(IndexedIntegral(A[i], A[j]))

