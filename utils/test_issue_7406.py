
def test_issue_7406():
    rng = np.random.default_rng(4763112764)
    assert_equal(binom.ppf(rng.random(10), 0, 0.5), 0)

    # Also check that endpoints (q=0, q=1) are correct
    assert_equal(binom.ppf(0, 0, 0.5), -1)
    assert_equal(binom.ppf(1, 0, 0.5), 0)

