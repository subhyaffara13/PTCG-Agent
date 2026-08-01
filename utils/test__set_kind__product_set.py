
def test_SetKind_ProductSet():
    p = ProductSet(FiniteSet(Matrix([1, 2])), FiniteSet(Matrix([1, 2])))
    mk = MatrixKind(NumberKind)
    k = SetKind(TupleKind(mk, mk))
    assert p.kind is k
    assert ProductSet(Interval(1, 2), FiniteSet(Matrix([1, 2]))).kind is SetKind(TupleKind(NumberKind, mk))

