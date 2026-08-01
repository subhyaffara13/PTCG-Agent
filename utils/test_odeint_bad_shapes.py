
def test_odeint_bad_shapes():
    # Tests of some errors that can occur with odeint.

    def badrhs(x, t):
        return [1, -1]

    def sys1(x, t):
        return -100*x

    def badjac(x, t):
        return [[0, 0, 0]]

    # y0 must be at most 1-d.
    bad_y0 = [[0, 0], [0, 0]]
    assert_raises(ValueError, odeint, sys1, bad_y0, [0, 1])

    # t must be at most 1-d.
    bad_t = [[0, 1], [2, 3]]
    assert_raises(ValueError, odeint, sys1, [10.0], bad_t)

    # y0 is 10, but badrhs(x, t) returns [1, -1].
    assert_raises(RuntimeError, odeint, badrhs, 10, [0, 1])

    # shape of array returned by badjac(x, t) is not correct.
    assert_raises(RuntimeError, odeint, sys1, [10, 10], [0, 1], Dfun=badjac)

