
def test_deltaproduct_trivial():
    assert dp(x, (j, 1, 0)) == 1
    assert dp(x, (j, 1, 3)) == x**3
    assert dp(x + y, (j, 1, 3)) == (x + y)**3
    assert dp(x*y, (j, 1, 3)) == (x*y)**3
    assert dp(KD(i, j), (k, 1, 3)) == KD(i, j)
    assert dp(x*KD(i, j), (k, 1, 3)) == x**3*KD(i, j)
    assert dp(x*y*KD(i, j), (k, 1, 3)) == (x*y)**3*KD(i, j)

