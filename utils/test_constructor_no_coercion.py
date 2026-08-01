
def test_constructor_no_coercion():
    with pytest.raises(ValueError, match="NumPy array"):
        NumpyExtensionArray([1, 2, 3])

