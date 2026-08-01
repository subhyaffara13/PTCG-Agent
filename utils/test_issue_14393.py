
def test_issue_14393():
    a, b = symbols('a b')
    assert limit((x**b - y**b)/(x**a - y**a), x, y) == b*y**(-a + b)/a

