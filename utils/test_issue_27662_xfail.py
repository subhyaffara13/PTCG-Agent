
def test_issue_27662_xfail():
    assert ask(Q.finite(x*y), ~Q.finite(x)
        & Q.zero(y)) is None

