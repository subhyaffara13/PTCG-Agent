
def test_deltasummation_mul_x_kd():
    assert ds(x*KD(i, j), (j, 1, 3)) == \
        Piecewise((x, And(1 <= i, i <= 3)), (0, True))
    assert ds(x*KD(i, j), (j, 1, 1)) == Piecewise((x, Eq(i, 1)), (0, True))
    assert ds(x*KD(i, j), (j, 2, 2)) == Piecewise((x, Eq(i, 2)), (0, True))
    assert ds(x*KD(i, j), (j, 3, 3)) == Piecewise((x, Eq(i, 3)), (0, True))
    assert ds(x*KD(i, j), (j, 1, k)) == \
        Piecewise((x, And(1 <= i, i <= k)), (0, True))
    assert ds(x*KD(i, j), (j, k, 3)) == \
        Piecewise((x, And(k <= i, i <= 3)), (0, True))
    assert ds(x*KD(i, j), (j, k, l)) == \
        Piecewise((x, And(k <= i, i <= l)), (0, True))

