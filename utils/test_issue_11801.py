
def test_issue_11801():
    assert pretty(Symbol("")) == ""
    assert upretty(Symbol("")) == ""

