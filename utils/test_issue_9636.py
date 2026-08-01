
def test_issue_9636():
    assert ask(Q.integer(1.0)) is None
    assert ask(Q.prime(3.0)) is None
    assert ask(Q.composite(4.0)) is None
    assert ask(Q.even(2.0)) is None
    assert ask(Q.odd(3.0)) is None

