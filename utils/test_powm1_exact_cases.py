
def test_powm1_exact_cases(x, y, expected):
    # Test cases where we have an exact expected value.
    p = powm1(x, y)
    assert p == expected

