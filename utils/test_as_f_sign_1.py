
def test_as_f_sign_1():
    assert as_f_sign_1(x + 1) == (1, x, 1)
    assert as_f_sign_1(x - 1) == (1, x, -1)
    assert as_f_sign_1(-x + 1) == (-1, x, -1)
    assert as_f_sign_1(-x - 1) == (-1, x, 1)
    assert as_f_sign_1(2*x + 2) == (2, x, 1)
    assert as_f_sign_1(x*y - y) == (y, x, -1)
    assert as_f_sign_1(-x*y + y) == (-y, x, -1)

