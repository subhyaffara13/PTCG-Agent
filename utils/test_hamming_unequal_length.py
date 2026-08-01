
def test_hamming_unequal_length():
    # Regression test for gh-4290.
    x = [0, 0, 1]
    y = [1, 0, 1, 0]
    # Used to give an AttributeError from ndarray.mean called on bool
    with pytest.raises(ValueError):
        whamming(x, y)

