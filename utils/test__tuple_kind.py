
def test_TupleKind():
    kind = TupleKind(NumberKind, MatrixKind(NumberKind))
    assert Tuple(1, Matrix([1, 2])).kind is kind
    assert Tuple(1, 2).kind is TupleKind(NumberKind, NumberKind)
    assert Tuple(1, 2).kind.element_kind == (NumberKind, NumberKind)

