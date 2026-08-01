
def test_period_index_construction_from_strings(klass):
    # https://github.com/pandas-dev/pandas/issues/26109
    strings = ["2020Q1", "2020Q2"] * 2
    data = klass(strings)
    result = PeriodIndex(data, freq="Q")
    expected = PeriodIndex([Period(s) for s in strings])
    tm.assert_index_equal(result, expected)

