
def test_invalid_dtype_string():
    # test for gh-10440
    assert_raises(TypeError, np.dtype, 'f8,i8,[f8,i8]')
    assert_raises(TypeError, np.dtype, 'Fl\xfcgel')

