
def test_assert_almost_equal_numbers_atol(a, b):
    # Equivalent to the deprecated check_less_precise=True, enforced in 2.0
    _assert_almost_equal_both(a, b, rtol=0.5e-3, atol=0.5e-3)

