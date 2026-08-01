
def test_issue_8444_nonworkingtests():
    x = symbols('x', real=True)
    assert (x <= oo) == (x >= -oo) == True

    x = symbols('x')
    assert x >= floor(x)
    assert (x < floor(x)) == False
    assert x <= ceiling(x)
    assert (x > ceiling(x)) == False

