
def test_Catalan_rewrite():
    k = Dummy('k', integer=True, nonnegative=True)
    assert Catalan.rewrite(Sum).dummy_eq(
            Sum((-1)**k/(2*k + 1)**2, (k, 0, oo)))
    assert Catalan.rewrite() == Catalan

