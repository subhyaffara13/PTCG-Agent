
def test_deltasummation_mul_add_x_y_kd():
    assert ds((x + y)*KD(i, j), (j, 1, 3)) == \
        Piecewise((x + y, And(1 <= i, i <= 3)), (0, True))
    assert ds((x + y)*KD(i, j), (j, 1, 1)) == \
        Piecewise((x + y, Eq(i, 1)), (0, True))
    assert ds((x + y)*KD(i, j), (j, 2, 2)) == \
        Piecewise((x + y, Eq(i, 2)), (0, True))
    assert ds((x + y)*KD(i, j), (j, 3, 3)) == \
        Piecewise((x + y, Eq(i, 3)), (0, True))
    assert ds((x + y)*KD(i, j), (j, 1, k)) == \
        Piecewise((x + y, And(1 <= i, i <= k)), (0, True))
    assert ds((x + y)*KD(i, j), (j, k, 3)) == \
        Piecewise((x + y, And(k <= i, i <= 3)), (0, True))
    assert ds((x + y)*KD(i, j), (j, k, l)) == \
        Piecewise((x + y, And(k <= i, i <= l)), (0, True))

