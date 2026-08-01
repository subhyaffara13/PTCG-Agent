
def test_interpolate_no_op(method):
    df = DataFrame({"a": [1, 2]})
    df_orig = df.copy()

    if method == "pad":
        msg = f"Can not interpolate with method={method}"
        with pytest.raises(ValueError, match=msg):
            df.interpolate(method=method)
    else:
        result = df.interpolate(method=method)
        assert np.shares_memory(get_array(result, "a"), get_array(df, "a"))
        assert result.index is not df.index
        assert result.columns is not df.columns

        result.iloc[0, 0] = 100

        assert not np.shares_memory(get_array(result, "a"), get_array(df, "a"))
        tm.assert_frame_equal(df, df_orig)

