
def test_issue_14470():
    assert integrate(1/sqrt(exp(x) + 1), x) == log(sqrt(exp(x) + 1) - 1) - log(sqrt(exp(x) + 1) + 1)


def test_issue_14470():
    assert_is_integral_of(1/(x*sqrt(x + 1)), log(sqrt(x + 1) - 1) - log(sqrt(x + 1) + 1))

