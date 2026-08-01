
def test_integer_array_numpy_sum(values, expected):
    arr = pd.array(values, dtype="Int64")
    result = np.sum(arr)
    assert result == expected

