
def test_issue_5833():
    assert ask(Q.positive(log(x)**2), Q.positive(x)) is None
    assert ask(~Q.negative(log(x)**2), Q.positive(x)) is True

