
def test_interpolate_downcast_reference_triggers_copy():
    df = DataFrame({"a": [1, np.nan, 2.5], "b": 1})
    df_orig = df.copy()
    arr_a = get_array(df, "a")
    view = df[:]

    msg = "Can not interpolate with method=pad"
    with pytest.raises(ValueError, match=msg):
        df.interpolate(method="pad", inplace=True)
        assert df._mgr._has_no_reference(0)
        assert not np.shares_memory(arr_a, get_array(df, "a"))

    tm.assert_frame_equal(df_orig, view)

