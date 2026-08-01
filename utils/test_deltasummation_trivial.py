
def test_deltasummation_trivial():
    assert ds(x, (j, 1, 0)) == 0
    assert ds(x, (j, 1, 3)) == 3*x
    assert ds(x + y, (j, 1, 3)) == 3*(x + y)
    assert ds(x*y, (j, 1, 3)) == 3*x*y
    assert ds(KD(i, j), (k, 1, 3)) == 3*KD(i, j)
    assert ds(x*KD(i, j), (k, 1, 3)) == 3*x*KD(i, j)
    assert ds(x*y*KD(i, j), (k, 1, 3)) == 3*x*y*KD(i, j)

