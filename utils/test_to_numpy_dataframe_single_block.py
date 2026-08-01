
def test_to_numpy_dataframe_single_block(data, expected_data):
    # https://github.com/pandas-dev/pandas/issues/33820
    df = pd.DataFrame(data)
    result = df.to_numpy(dtype=float, na_value=np.nan)
    expected = np.array(expected_data, dtype=float)
    tm.assert_numpy_array_equal(result, expected)

