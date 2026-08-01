
def test_interpolate_object_convert_copies():
    df = DataFrame({"a": [1, np.nan, 2.5], "b": 1})
    arr_a = get_array(df, "a")
    msg = "Can not interpolate with method=pad"
    with pytest.raises(ValueError, match=msg):
        df.interpolate(method="pad", inplace=True)

    assert df._mgr._has_no_reference(0)
    assert np.shares_memory(arr_a, get_array(df, "a"))

