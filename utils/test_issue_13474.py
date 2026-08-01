
def test_issue_13474():
    x = Symbol('x')
    assert simplify(x + csch(sinc(1))) == x + csch(sinc(1))

