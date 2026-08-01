
def test_to_numpy_with_defaults(data, using_nan_is_na):
    # GH49973
    result = data.to_numpy()

    pa_type = data._pa_array.type
    if pa.types.is_duration(pa_type) or pa.types.is_timestamp(pa_type):
        pytest.skip("Tested in test_to_numpy_temporal")
    elif pa.types.is_date(pa_type):
        expected = np.array(list(data))
    else:
        expected = np.array(data._pa_array)

    if data._hasna and (not is_numeric_dtype(data.dtype) or not using_nan_is_na):
        expected = expected.astype(object)
        expected[pd.isna(data)] = pd.NA

    tm.assert_numpy_array_equal(result, expected)

