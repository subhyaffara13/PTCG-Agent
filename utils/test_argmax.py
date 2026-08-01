
def test_argmax(strings):
    """Test that argmax/argmin matches what python calculates."""
    arr = np.array(strings, dtype="T")
    assert np.argmax(arr) == strings.index(max(strings))
    assert np.argmin(arr) == strings.index(min(strings))

