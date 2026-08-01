
def test_categorical_to_numpy_dlpack():
    # https://github.com/pandas-dev/pandas/issues/48393
    df = pd.DataFrame({"A": pd.Categorical(["a", "b", "a"])})
    with tm.assert_produces_warning(match="Interchange"):
        col = df.__dataframe__().get_column_by_name("A")
    result = np.from_dlpack(col.get_buffers()["data"][0])
    expected = np.array([0, 1, 0], dtype="int8")
    tm.assert_numpy_array_equal(result, expected)

