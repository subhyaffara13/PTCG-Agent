
def test_resample_extra_index_point(unit):
    # GH#9756
    index = date_range(start="20150101", end="20150331", freq="BME").as_unit(unit)
    expected = DataFrame({"A": Series([21, 41, 63], index=index)})

    index = date_range(start="20150101", end="20150331", freq="B").as_unit(unit)
    df = DataFrame({"A": Series(range(len(index)), index=index)}, dtype="int64")
    result = df.resample("BME").last()
    tm.assert_frame_equal(result, expected)

