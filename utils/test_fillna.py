
def test_fillna(index_or_series_obj):
    # GH 11343
    obj = index_or_series_obj

    if isinstance(obj, MultiIndex):
        msg = "fillna is not defined for MultiIndex"
        with pytest.raises(NotImplementedError, match=msg):
            obj.fillna(0)
        return

    # values will not be changed
    fill_value = obj.values[0] if len(obj) > 0 else 0
    result = obj.fillna(fill_value)

    tm.assert_equal(obj, result)

    # check shallow_copied
    assert obj is not result


def test_fillna():
    df = DataFrame({"a": [1.5, np.nan], "b": 1})
    df_orig = df.copy()

    df2 = df.fillna(5.5)
    assert np.shares_memory(get_array(df, "b"), get_array(df2, "b"))
    assert df2.index is not df.index
    assert df2.columns is not df.columns

    df2.iloc[0, 1] = 100
    tm.assert_frame_equal(df_orig, df)


def test_fillna(idx):
    # GH 11343
    msg = "fillna is not defined for MultiIndex"
    with pytest.raises(NotImplementedError, match=msg):
        idx.fillna(idx[0])

