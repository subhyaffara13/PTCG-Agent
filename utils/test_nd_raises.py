
def test_nd_raises(data):
    with pytest.raises(ValueError, match="NumpyExtensionArray must be 1-dimensional"):
        pd.array(data, dtype="int64")

