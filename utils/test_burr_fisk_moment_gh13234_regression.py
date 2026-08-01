
def test_burr_fisk_moment_gh13234_regression():
    vals0 = stats.burr.moment(1, 5, 4)
    assert isinstance(vals0, float)

    vals1 = stats.fisk.moment(1, 8)
    assert isinstance(vals1, float)

