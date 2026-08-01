
def test_issue_5615():
    aA, Re, a, b, D = symbols('aA Re a b D')
    e = ((D**3*a + b*aA**3)/Re).expand()
    assert collect(e, [aA**3/Re, a]) == e

