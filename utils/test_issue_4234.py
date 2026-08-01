
def test_issue_4234():
    assert integrate(1/sqrt(1 + tan(x)**2)) == tan(x)/sqrt(1 + tan(x)**2)

