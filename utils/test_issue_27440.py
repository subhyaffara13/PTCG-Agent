
def test_issue_27440():
    nan = S.NaN
    assert ask(Q.negative(nan)) is None

