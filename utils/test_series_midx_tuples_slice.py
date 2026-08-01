
def test_series_midx_tuples_slice():
    ser = Series(
        [1, 2, 3],
        index=pd.MultiIndex.from_tuples([((1, 2), 3), ((1, 2), 4), ((2, 3), 4)]),
    )
    result = ser[(1, 2)]
    assert np.shares_memory(get_array(ser), get_array(result))
    result.iloc[0] = 100
    expected = Series(
        [1, 2, 3],
        index=pd.MultiIndex.from_tuples([((1, 2), 3), ((1, 2), 4), ((2, 3), 4)]),
    )
    tm.assert_series_equal(ser, expected)

