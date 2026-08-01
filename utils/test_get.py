
def test_get():
    assert get(1, 'ABCDE') == 'B'
    assert list(get([1, 3], 'ABCDE')) == list('BD')
    assert get('a', {'a': 1, 'b': 2, 'c': 3}) == 1
    assert get(['a', 'b'], {'a': 1, 'b': 2, 'c': 3}) == (1, 2)

    assert get('foo', {}, default='bar') == 'bar'
    assert get({}, [1, 2, 3], default='bar') == 'bar'
    assert get([0, 2], 'AB', 'C') == ('A', 'C')

    assert get([0], 'AB') == ('A',)
    assert get([], 'AB') == ()

    assert raises(IndexError, lambda: get(10, 'ABC'))
    assert raises(KeyError, lambda: get(10, {'a': 1}))
    assert raises(TypeError, lambda: get({}, [1, 2, 3]))
    assert raises(TypeError, lambda: get([1, 2, 3], 1, None))
    assert raises(KeyError, lambda: get('foo', {}, default=no_default2))


def test_get(d, Asp):
    assert Asp.get((0, 1)) == d.get((0, 1))
    assert Asp.get((0, 0), 99) == d.get((0, 0), 99)
    with pytest.raises(IndexError, match="out of bounds"):
        Asp.get((0, 4), 99)


def test_get(key):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df_orig = df.copy()

    result = df.get(key)

    assert np.shares_memory(get_array(result, "a"), get_array(df, "a"))
    result.iloc[0] = 0
    assert not np.shares_memory(get_array(result, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)


def test_get():
    ser = Series(["a_b_c", "c_d_e", np.nan, "f_g_h"])
    result = ser.str.split("_").str.get(1)
    expected = Series(["b", "d", np.nan, "g"], dtype=object)
    tm.assert_series_equal(result, expected)


def test_get():
    # GH 6383
    s = Series(
        np.array(
            [
                43,
                48,
                60,
                48,
                50,
                51,
                50,
                45,
                57,
                48,
                56,
                45,
                51,
                39,
                55,
                43,
                54,
                52,
                51,
                54,
            ]
        )
    )

    result = s.get(25, 0)
    expected = 0
    assert result == expected

    s = Series(
        np.array(
            [
                43,
                48,
                60,
                48,
                50,
                51,
                50,
                45,
                57,
                48,
                56,
                45,
                51,
                39,
                55,
                43,
                54,
                52,
                51,
                54,
            ]
        ),
        index=Index(
            [
                25.0,
                36.0,
                49.0,
                64.0,
                81.0,
                100.0,
                121.0,
                144.0,
                169.0,
                196.0,
                1225.0,
                1296.0,
                1369.0,
                1444.0,
                1521.0,
                1600.0,
                1681.0,
                1764.0,
                1849.0,
                1936.0,
            ],
            dtype=np.float64,
        ),
    )

    result = s.get(25, 0)
    expected = 43
    assert result == expected

    # GH 7407
    # with a boolean accessor
    df = pd.DataFrame({"i": [0] * 3, "b": [False] * 3})
    vc = df.i.value_counts()
    result = vc.get(99, default="Missing")
    assert result == "Missing"

    vc = df.b.value_counts()
    result = vc.get(False, default="Missing")
    assert result == 3

    result = vc.get(True, default="Missing")
    assert result == "Missing"


def test_get(temp_hdfstore):
    temp_hdfstore["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    left = temp_hdfstore.get("a")
    right = temp_hdfstore["a"]
    tm.assert_series_equal(left, right)

    left = temp_hdfstore.get("/a")
    right = temp_hdfstore["/a"]
    tm.assert_series_equal(left, right)

    with pytest.raises(KeyError, match="'No object named b in the file'"):
        temp_hdfstore.get("b")

