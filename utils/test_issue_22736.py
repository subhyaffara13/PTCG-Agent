
def test_issue_22736():
    a = CRootOf(x**4 + x**3 + x**2 + x + 1, -1)
    a._reset()
    b = exp(2*I*pi/5)
    assert field_isomorphism(a, b) == [1, 0]

