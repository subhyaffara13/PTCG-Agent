
def test_issue_17137():
    assert simplify(cos(x)**I) == cos(x)**I
    assert simplify(cos(x)**(2 + 3*I)) == cos(x)**(2 + 3*I)

