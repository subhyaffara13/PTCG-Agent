
def test_issue_4788():
    assert srepr(S(1.0 + 0J)) == srepr(S(1.0)) == srepr(Float(1.0))

