
def test_attributes():
    assert sin(x).args == (x,)


def test_attributes(xp):
    A = interface.aslinearoperator(xp.reshape(xp.arange(16, dtype=xp.float64), (4, 4)))

    def always_four_ones(x):
        x = xp.asarray(x)
        assert x.shape == (3,) or x.shape == (3, 1)
        return xp.ones(4)

    B = interface.LinearOperator(shape=(4, 3), matvec=always_four_ones, xp=xp)

    ops = [A, B, A * B, A @ B, A.H, A.adjoint(), A + A, B + B, A**4]
    for op in ops:
        assert hasattr(op, "dtype")
        assert hasattr(op, "shape")
        assert hasattr(op, "_matvec")


def test_attributes():
   #assert hasattr(module, "a") and module.a == 1234  #FIXME: -m dill.tests
    assert module.double_add(1, 2, 3) == 2 * module.fx

