
def test_issue_4494():
    a, b = symbols('a b')
    eq = sin(a)**2*sin(b)**2 + cos(a)**2*cos(b)**2*tan(a)**2 + cos(a)**2
    assert trigsimp(eq) == 1

