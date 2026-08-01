
def test_from_arrays_different_lengths(idx1, idx2):
    # see gh-13599
    msg = "^all arrays must be same length$"
    with pytest.raises(ValueError, match=msg):
        MultiIndex.from_arrays([idx1, idx2])

