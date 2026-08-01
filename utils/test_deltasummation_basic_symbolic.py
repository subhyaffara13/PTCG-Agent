
def test_deltasummation_basic_symbolic():
    assert ds(KD(i, j), (j, 1, 3)) == \
        Piecewise((1, And(1 <= i, i <= 3)), (0, True))
    assert ds(KD(i, j), (j, 1, 1)) == Piecewise((1, Eq(i, 1)), (0, True))
    assert ds(KD(i, j), (j, 2, 2)) == Piecewise((1, Eq(i, 2)), (0, True))
    assert ds(KD(i, j), (j, 3, 3)) == Piecewise((1, Eq(i, 3)), (0, True))
    assert ds(KD(i, j), (j, 1, k)) == \
        Piecewise((1, And(1 <= i, i <= k)), (0, True))
    assert ds(KD(i, j), (j, k, 3)) == \
        Piecewise((1, And(k <= i, i <= 3)), (0, True))
    assert ds(KD(i, j), (j, k, l)) == \
        Piecewise((1, And(k <= i, i <= l)), (0, True))

