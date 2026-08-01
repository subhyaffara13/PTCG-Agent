
def test_to_numpy_dataframe_single_block_no_mutate():
    # https://github.com/pandas-dev/pandas/issues/33820
    result = pd.DataFrame(np.array([1.0, 2.0, np.nan]))
    expected = pd.DataFrame(np.array([1.0, 2.0, np.nan]))
    result.to_numpy(na_value=0.0)
    tm.assert_frame_equal(result, expected)

