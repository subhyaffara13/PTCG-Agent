
def test_findall_mixed_object():
    ser = Series(
        [
            "fooBAD__barBAD",
            np.nan,
            "foo",
            True,
            datetime.today(),
            "BAD",
            None,
            1,
            2.0,
        ]
    )

    result = ser.str.findall("BAD[_]*")
    expected = Series(
        [
            ["BAD__", "BAD"],
            np.nan,
            [],
            np.nan,
            np.nan,
            ["BAD"],
            None,
            np.nan,
            np.nan,
        ]
    )

    tm.assert_series_equal(result, expected)

