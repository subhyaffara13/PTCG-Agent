
def test_generic_identity():
    assert MatAdd.identity == GenericZeroMatrix()
    assert MatAdd.identity != S.Zero


def test_generic_identity():
    assert MatMul.identity == GenericIdentity()
    assert MatMul.identity != S.One


def test_generic_identity():
    I = GenericIdentity()
    n = symbols('n', integer=True)
    A = MatrixSymbol("A", n, n)

    assert I == I
    assert I != A
    assert A != I

    assert I.is_Identity
    assert I**-1 == I

    raises(TypeError, lambda: I.shape)
    raises(TypeError, lambda: I.rows)
    raises(TypeError, lambda: I.cols)

    assert MatMul() == I
    assert MatMul(I, A) == MatMul(A)
    # Make sure it is hashable
    hash(I)

