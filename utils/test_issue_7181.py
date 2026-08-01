
def test_issue_7181():
    assert mellin_transform(1/(1 - x), x, s) != None

