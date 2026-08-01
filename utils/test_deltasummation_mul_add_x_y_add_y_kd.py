
def test_deltasummation_mul_add_x_y_add_y_kd():
    assert ds((x + y)*(y + KD(i, j)), (j, 1, 3)) == Piecewise(
        (3*(x + y)*y + x + y, And(1 <= i, i <= 3)), (3*(x + y)*y, True))
    assert ds((x + y)*(y + KD(i, j)), (j, 1, 1)) == \
        Piecewise(((x + y)*y + x + y, Eq(i, 1)), ((x + y)*y, True))
    assert ds((x + y)*(y + KD(i, j)), (j, 2, 2)) == \
        Piecewise(((x + y)*y + x + y, Eq(i, 2)), ((x + y)*y, True))
    assert ds((x + y)*(y + KD(i, j)), (j, 3, 3)) == \
        Piecewise(((x + y)*y + x + y, Eq(i, 3)), ((x + y)*y, True))
    assert ds((x + y)*(y + KD(i, j)), (j, 1, k)) == Piecewise(
        (k*(x + y)*y + x + y, And(1 <= i, i <= k)), (k*(x + y)*y, True))
    assert ds((x + y)*(y + KD(i, j)), (j, k, 3)) == Piecewise(
        ((4 - k)*(x + y)*y + x + y, And(k <= i, i <= 3)),
        ((4 - k)*(x + y)*y, True))
    assert ds((x + y)*(y + KD(i, j)), (j, k, l)) == Piecewise(
        ((l - k + 1)*(x + y)*y + x + y, And(k <= i, i <= l)),
        ((l - k + 1)*(x + y)*y, True))

