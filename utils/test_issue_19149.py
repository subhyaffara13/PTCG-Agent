
def test_issue_19149():
    eq = exp(3*x/4)
    assert collect(eq, exp(x)) == eq

