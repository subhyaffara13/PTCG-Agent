
def test_resampler_is_iterable(index):
    # GH 15314
    series = Series(range(len(index)), index=index)
    freq = "h"
    tg = Grouper(freq=freq, convention="start")
    grouped = series.groupby(tg)
    resampled = series.resample(freq)
    for (rk, rv), (gk, gv) in zip(resampled, grouped):
        assert rk == gk
        tm.assert_series_equal(rv, gv)

