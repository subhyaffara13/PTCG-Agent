
def test_npy_char_raises():
    from numpy._core._multiarray_tests import npy_char_deprecation
    with pytest.raises(ValueError):
        npy_char_deprecation()

