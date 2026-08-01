
def test_issue_14454():
    number = CRootOf(x**4 + x - 1, 2)
    raises(ValueError, lambda: invert_real(number, 0, x))
    assert invert_real(x**2, number, x)  # no error

