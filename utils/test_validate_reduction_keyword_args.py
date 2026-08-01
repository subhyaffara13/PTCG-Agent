
def test_validate_reduction_keyword_args():
    arr = NumpyExtensionArray(np.array([1, 2, 3]))
    msg = "the 'keepdims' parameter is not supported .*all"
    with pytest.raises(ValueError, match=msg):
        arr.all(keepdims=True)

