
def test_fail_mmap():
    with pytest.raises(UnsupportedOperation, match="fileno"):
        with BytesIO() as buffer:
            icom.get_handle(buffer, "rb", memory_map=True)

