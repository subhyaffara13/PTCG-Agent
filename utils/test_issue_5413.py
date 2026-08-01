
def test_issue_5413():
    # Note that this is not the same as testing ratint() because integrate()
    # pulls out the coefficient.
    assert integrate(-a/(a**2 + x**2), x) == I*log(-I*a + x)/2 - I*log(I*a + x)/2

