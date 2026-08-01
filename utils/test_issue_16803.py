
def test_issue_16803():
    n = symbols('n')
    # No simplification done, but should not raise an exception
    assert ((n > 3) | (n < 0) | ((n > 0) & (n < 3))).simplify() == \
           (n > 3) | (n < 0) | ((n > 0) & (n < 3))

