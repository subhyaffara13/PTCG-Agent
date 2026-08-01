
def test_P11_workaround():
    # This test was changed to inverse method ADJ because it depended on the
    # specific form of inverse returned from the 'GE' method which has changed.
    M = Matrix([[x, y], [1, x*y]]).inv('ADJ')
    c = gcd(tuple(M))
    assert MatMul(c, M/c, evaluate=False) == MatMul(c, Matrix([
        [x*y, -y],
        [ -1,  x]]), evaluate=False)

