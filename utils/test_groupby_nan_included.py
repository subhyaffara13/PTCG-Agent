
def test_groupby_nan_included():
    # GH 35646
    data = {"group": ["g1", np.nan, "g1", "g2", np.nan], "B": [0, 1, 2, 3, 4]}
    df = pd.DataFrame(data)
    grouped = df.groupby("group", dropna=False)
    result = grouped.indices
    dtype = np.intp
    expected = {
        "g1": np.array([0, 2], dtype=dtype),
        "g2": np.array([3], dtype=dtype),
        np.nan: np.array([1, 4], dtype=dtype),
    }
    for result_values, expected_values in zip(
        result.values(), expected.values(), strict=True
    ):
        tm.assert_numpy_array_equal(result_values, expected_values)
    assert np.isnan(list(result.keys())[2])
    assert list(result.keys())[0:2] == ["g1", "g2"]

