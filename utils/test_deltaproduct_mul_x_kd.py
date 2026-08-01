
def test_deltaproduct_mul_x_kd():
    assert dp(x*KD(i, j), (j, 1, 3)) == 0
    assert dp(x*KD(i, j), (j, 1, 1)) == x*KD(i, 1)
    assert dp(x*KD(i, j), (j, 2, 2)) == x*KD(i, 2)
    assert dp(x*KD(i, j), (j, 3, 3)) == x*KD(i, 3)
    assert dp(x*KD(i, j), (j, 1, k)) == x*KD(i, 1)*KD(k, 1) + KD(k, 0)
    assert dp(x*KD(i, j), (j, k, 3)) == x*KD(i, 3)*KD(k, 3) + KD(k, 4)
    assert dp(x*KD(i, j), (j, k, l)) == x*KD(i, l)*KD(k, l) + KD(k, l + 1)

