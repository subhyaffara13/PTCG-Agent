
def test_odeint_trivial_time():
    # Test that odeint succeeds when given a single time point
    # and full_output=True.  This is a regression test for gh-4282.
    y0 = 1
    t = [0]
    y, info = odeint(lambda y, t: -y, y0, t, full_output=True)
    assert_array_equal(y, np.array([[y0]]))

