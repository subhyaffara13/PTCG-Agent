
def test_as_explicit():
    c0, c1, c2 = symbols('c0:3')
    x = Symbol('x')
    assert CompanionMatrix(Poly([1, c0], x)).as_explicit() == \
        ImmutableDenseMatrix([-c0])
    assert CompanionMatrix(Poly([1, c1, c0], x)).as_explicit() == \
        ImmutableDenseMatrix([[0, -c0], [1, -c1]])
    assert CompanionMatrix(Poly([1, c2, c1, c0], x)).as_explicit() == \
        ImmutableDenseMatrix([[0, 0, -c0], [1, 0, -c1], [0, 1, -c2]])


def test_as_explicit():
    Z = MatrixSymbol('Z', 2, 3)
    assert Z.as_explicit() == ImmutableMatrix([
        [Z[0, 0], Z[0, 1], Z[0, 2]],
        [Z[1, 0], Z[1, 1], Z[1, 2]],
    ])
    raises(ValueError, lambda: A.as_explicit())

