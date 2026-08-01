
def test_trigsimp_issue_3826():
    assert trigsimp(tan(2*x).expand(trig=True)) == tan(2*x)

