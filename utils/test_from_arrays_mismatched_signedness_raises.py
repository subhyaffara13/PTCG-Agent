
def test_from_arrays_mismatched_signedness_raises():
    # GH 55715
    left = np.array([0, 1, 2], dtype="int64")
    right = np.array([1, 2, 3], dtype="uint64")
    with pytest.raises(TypeError, match="matching signedness"):
        IntervalIndex.from_arrays(left, right)

