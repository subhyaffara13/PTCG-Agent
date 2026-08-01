
def test_blitting_events(env):
    proc = _run_helper(
        _test_number_of_draws_script, timeout=_test_timeout, extra_env=env)
    # Count the number of draw_events we got. We could count some initial
    # canvas draws (which vary in number by backend), but the critical
    # check here is that it isn't 10 draws, which would be called if
    # blitting is not properly implemented
    ndraws = proc.stdout.count("DrawEvent")
    assert 0 < ndraws < 5

