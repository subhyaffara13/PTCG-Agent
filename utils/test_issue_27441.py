
def test_issue_27441():
    # https://github.com/sympy/sympy/issues/27441
    assert ask(Q.composite(y), Q.integer(y) & Q.positive(y) & ~Q.prime(y)) is None

