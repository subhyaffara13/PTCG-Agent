
def test_issue_7903():
    a = symbols(r'a', real=True)
    t = exp(I*cos(a)) + exp(-I*sin(a))
    assert t.simplify()

