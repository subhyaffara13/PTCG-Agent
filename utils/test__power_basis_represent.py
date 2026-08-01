
def test_PowerBasis_represent():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    col = to_col([1, 2, 3, 4])
    a = A(col)
    assert A.represent(a) == col
    b = A(col, denom=2)
    raises(ClosureFailure, lambda: A.represent(b))

