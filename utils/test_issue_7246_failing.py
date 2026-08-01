
def test_issue_7246_failing():
    #Move this test to test_issue_7246 once
    #the new assumptions module is improved.
    assert ask(Q.positive(acos(x)), Q.zero(x)) is True

