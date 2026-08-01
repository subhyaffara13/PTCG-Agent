
def test_close_on_error():
    # GH 47136
    class TestError:
        def close(self):
            raise OSError("test")

    with pytest.raises(OSError, match="test"):
        with BytesIO() as buffer:
            with icom.get_handle(buffer, "rb") as handles:
                handles.created_handles.append(TestError())

