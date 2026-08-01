
def test_gh_19103():
    # Checks that least_squares trf method selects a strictly feasible point,
    # and thus succeeds instead of failing,
    # when the initial guess is reported exactly at a boundary point.
    # This is a reduced example from gh191303

    ydata = np.array([0.] * 66 + [
        1., 0., 0., 0., 0., 0., 1., 1., 0., 0., 1.,
        1., 1., 1., 0., 0., 0., 1., 0., 0., 2., 1.,
        0., 3., 1., 6., 5., 0., 0., 2., 8., 4., 4.,
        6., 9., 7., 2., 7., 8., 2., 13., 9., 8., 11.,
        10., 13., 14., 19., 11., 15., 18., 26., 19., 32., 29.,
        28., 36., 32., 35., 36., 43., 52., 32., 58., 56., 52.,
        67., 53., 72., 88., 77., 95., 94., 84., 86., 101., 107.,
        108., 118., 96., 115., 138., 137.,
    ])
    xdata = np.arange(0, ydata.size) * 0.1

    def exponential_wrapped(params):
        A, B, x0 = params
        return A * np.exp(B * (xdata - x0)) - ydata

    x0 = [0.01, 1., 5.]
    bounds = ((0.01, 0, 0), (np.inf, 10, 20.9))
    res = least_squares(exponential_wrapped, x0, method='trf', bounds=bounds)
    assert res.success

