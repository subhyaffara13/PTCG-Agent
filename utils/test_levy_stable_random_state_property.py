
def test_levy_stable_random_state_property():
    # levy_stable only implements rvs(), so it is skipped in the
    # main loop in test_cont_basic(). Here we apply just the test
    # check_random_state_property to levy_stable.
    check_random_state_property(stats.levy_stable, (0.5, 0.1))

