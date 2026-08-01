
def test_array_to_numpy_na():
    # GH#40638
    arr = pd.array([pd.NA, 1], dtype="string[python]")
    result = arr.to_numpy(na_value=True, dtype=bool)
    expected = np.array([True, True])
    tm.assert_numpy_array_equal(result, expected)

