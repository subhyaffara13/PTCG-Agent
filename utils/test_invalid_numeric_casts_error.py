
def test_invalid_numeric_casts_error(dtype, invalid):
    arr = np.array([invalid], dtype="T")

    with pytest.raises(ValueError):
        arr.astype(dtype)

