
def test_resample_anchored_multiday(label, sec):
    # When resampling a range spanning multiple days, ensure that the
    # start date gets used to determine the offset.  Fixes issue where
    # a one day period is not a multiple of the frequency.
    #
    # See: https://github.com/pandas-dev/pandas/issues/8683

    index1 = date_range("2014-10-14 23:06:23.206", periods=3, freq="400ms")
    index2 = date_range("2014-10-15 23:00:00", periods=2, freq="2200ms")
    index = index1.union(index2)

    s = Series(np.random.default_rng(2).standard_normal(5), index=index)

    # Ensure left closing works
    result = s.resample("2200ms", label=label).mean()
    assert result.index[-1] == Timestamp(f"2014-10-15 23:00:{sec}00")

