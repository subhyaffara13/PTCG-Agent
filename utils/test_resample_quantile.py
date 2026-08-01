
def test_resample_quantile(index):
    # GH 15023
    ser = Series(range(len(index)), index=index)
    q = 0.75
    freq = "h"

    result = ser.resample(freq).quantile(q)
    expected = ser.resample(freq).agg(lambda x: x.quantile(q)).rename(ser.name)
    tm.assert_series_equal(result, expected)

