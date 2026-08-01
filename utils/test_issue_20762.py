
def test_issue_20762():
    # Make sure pycode removes curly braces from subscripted variables
    a_b, b, a_11 = symbols('a_{b} b a_{11}')
    expr = a_b*b
    assert pycode(expr) == 'a_b*b'
    expr = a_11*b
    assert pycode(expr) == 'a_11*b'


def test_issue_20762():
    # Make sure Python removes curly braces from subscripted variables
    a_b = Symbol('a_{b}')
    b = Symbol('b')
    expr = a_b*b
    assert python(expr) == "a_b = Symbol('a_{b}')\nb = Symbol('b')\ne = a_b*b"

