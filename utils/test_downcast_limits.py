
def test_downcast_limits(dtype, downcast, min_max):
    # see gh-14404: test the limits of each downcast.
    series = to_numeric(Series(min_max), downcast=downcast)
    assert series.dtype == dtype

