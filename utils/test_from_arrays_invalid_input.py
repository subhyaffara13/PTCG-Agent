
def test_from_arrays_invalid_input(invalid_sequence_of_arrays):
    msg = "Input must be a list / sequence of array-likes"
    with pytest.raises(TypeError, match=msg):
        MultiIndex.from_arrays(arrays=invalid_sequence_of_arrays)

