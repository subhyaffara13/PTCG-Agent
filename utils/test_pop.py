
def test_pop(d, Asp):
    assert d.pop((0, 1)) == 1
    assert Asp.pop((0, 1)) == 1
    assert d.items() == Asp.items()

    assert Asp.pop((22, 21), None) is None
    assert Asp.pop((22, 21), "other") == "other"
    with pytest.raises(KeyError, match="(22, 21)"):
        Asp.pop((22, 21))
    msg = "got some positional-only arguments passed as keyword arguments: 'default'"
    with pytest.raises(TypeError, match=msg):
        Asp.pop((22, 21), default=5)


def test_pop():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()
    view_original = df[:]
    result = df.pop("a")

    assert np.shares_memory(result.values, get_array(view_original, "a"))
    assert np.shares_memory(get_array(df, "b"), get_array(view_original, "b"))

    result.iloc[0] = 0
    assert not np.shares_memory(result.values, get_array(view_original, "a"))
    df.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df, "b"), get_array(view_original, "b"))
    tm.assert_frame_equal(view_original, df_orig)


def test_pop():
    # GH#6600
    ser = Series([0, 4, 0], index=["A", "B", "C"], name=4)

    result = ser.pop("B")
    assert result == 4

    expected = Series([0, 0], index=["A", "C"], name=4)
    tm.assert_series_equal(ser, expected)

