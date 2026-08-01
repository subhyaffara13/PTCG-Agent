
def test_as_leading_term3():
    assert (2 + pi + x).as_leading_term(x) == 2 + pi
    assert (2*x + pi*x + x**2).as_leading_term(x) == 2*x + pi*x

