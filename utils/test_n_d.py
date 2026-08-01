
def test_nD(solver, xp):
    """Check that >2-D operators are rejected cleanly."""
    def id(x):
        return x
    A = LinearOperator(shape=(2, 2, 2), matvec=id, dtype=xp.float64, xp=xp)
    b = xp.ones((2, 2))
    with pytest.raises(ValueError, match="expected 2-D"):
        solver(A, b)


def test_nD():
    """Check that >2-D operators are rejected cleanly."""
    def id(x):
        return x
    A = LinearOperator(shape=(2, 2, 2), matvec=id, dtype=np.float64)
    b = np.ones((2, 2))
    with pytest.raises(ValueError, match="expected 2-D"):
        lsmr(A, b)


def test_nD():
    """Check that >2-D operators are rejected cleanly."""
    def id(x):
        return x
    A = LinearOperator(shape=(2, 2, 2), matvec=id, dtype=np.float64)
    b = np.ones((2, 2))
    with pytest.raises(ValueError, match="expected 2-D"):
        lsqr(A, b)


def test_nD(func):
    """Check that >2-D operators are rejected cleanly."""
    def id(x):
        return x
    A = LinearOperator(shape=(2, 2, 2), matvec=id, dtype=np.float64)
    with pytest.raises(ValueError, match="expected 2-D"):
        func(A)

