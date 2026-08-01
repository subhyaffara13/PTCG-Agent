
def test_test_memoryview_from_buffer_invalid_strides():
    with pytest.raises(RuntimeError):
        m.test_memoryview_from_buffer_invalid_strides()

