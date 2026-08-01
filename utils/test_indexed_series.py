
def test_indexed_series():
    A = IndexedBase("A")
    i = symbols("i", integer=True)
    assert sin(A[i]).series(A[i]) == A[i] - A[i]**3/6 + A[i]**5/120 + Order(A[i]**6, A[i])

