
def test_floating_array_numpy_sum(values, expected):
    arr = pd.array(values, dtype="Float64")
    result = np.sum(arr)
    assert result == expected

