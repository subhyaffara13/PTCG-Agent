
def test_deltasummation_basic_numerical():
    n = symbols('n', integer=True, nonzero=True)
    assert ds(KD(n, 0), (n, 1, 3)) == 0

    # return unevaluated, until it gets implemented
    assert ds(KD(i**2, j**2), (j, -oo, oo)) == \
        Sum(KD(i**2, j**2), (j, -oo, oo))

    assert Piecewise((KD(i, k), And(1 <= i, i <= 3)), (0, True)) == \
        ds(KD(i, j)*KD(j, k), (j, 1, 3)) == \
        ds(KD(j, k)*KD(i, j), (j, 1, 3))

    assert ds(KD(i, k), (k, -oo, oo)) == 1
    assert ds(KD(i, k), (k, 0, oo)) == Piecewise((1, S.Zero <= i), (0, True))
    assert ds(KD(i, k), (k, 1, 3)) == \
        Piecewise((1, And(1 <= i, i <= 3)), (0, True))
    assert ds(k*KD(i, j)*KD(j, k), (k, -oo, oo)) == j*KD(i, j)
    assert ds(j*KD(i, j), (j, -oo, oo)) == i
    assert ds(i*KD(i, j), (i, -oo, oo)) == j
    assert ds(x, (i, 1, 3)) == 3*x
    assert ds((i + j)*KD(i, j), (j, -oo, oo)) == 2*i

