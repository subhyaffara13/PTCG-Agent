
def test_kaiser_beta():
    b = kaiser_beta(58.7)
    assert_almost_equal(b, 0.1102 * 50.0)
    b = kaiser_beta(22.0)
    assert_almost_equal(b, 0.5842 + 0.07886)
    b = kaiser_beta(21.0)
    assert b == 0.0
    b = kaiser_beta(10.0)
    assert b == 0.0

