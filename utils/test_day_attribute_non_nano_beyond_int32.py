
def test_day_attribute_non_nano_beyond_int32():
    # GH 52386
    data = np.array(
        [
            136457654736252,
            134736784364431,
            245345345545332,
            223432411,
            2343241,
            3634548734,
            23234,
        ],
        dtype="timedelta64[s]",
    )
    ser = Series(data)
    result = ser.dt.days
    expected = Series([1579371003, 1559453522, 2839645203, 2586, 27, 42066, 0])
    tm.assert_series_equal(result, expected)

