
def test_broadcast_gh7933_regression():
    # Check broadcast works
    stats.truncnorm.logpdf(
        np.array([3.0, 2.0, 1.0]),
        a=(1.5 - np.array([6.0, 5.0, 4.0])) / 3.0,
        b=np.inf,
        loc=np.array([6.0, 5.0, 4.0]),
        scale=3.0
    )

