
def test_creating_dtype_with_dtype_class_errors():
    # Regression test for #25031, calling `np.dtype` with itself segfaulted.
    with pytest.raises(TypeError, match="Cannot convert np.dtype into a"):
        np.array(np.ones(10), dtype=np.dtype)

