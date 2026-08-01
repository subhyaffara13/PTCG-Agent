
def test_overlap():
    X = Normal('x', 0, 1)
    Y = Normal('x', 0, 2)

    raises(ValueError, lambda: P(X > Y))


def test_overlap():
    a = np.arange(9, dtype=int).reshape(3, 3)
    b = np.arange(9, dtype=int).reshape(3, 3)
    d = np.dot(a, b)
    # sanity check
    c = np.einsum('ij,jk->ik', a, b)
    assert_equal(c, d)
    # gh-10080, out overlaps one of the operands
    c = np.einsum('ij,jk->ik', a, b, out=b)
    assert_equal(c, d)

