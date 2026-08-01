
def test_issue_10927():
    x = symbols('x')
    assert str(Eq(x, oo)) == 'Eq(x, oo)'
    assert str(Eq(x, -oo)) == 'Eq(x, -oo)'

