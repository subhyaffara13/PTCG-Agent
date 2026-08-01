
def test_issue_1603():
    assert_equal(binom(1000, np.logspace(-3, -100)).ppf(0.01), 0)

