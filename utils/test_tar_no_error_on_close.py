
def test_tar_no_error_on_close():
    with io.BytesIO() as buffer:
        with icom._BytesTarFile(fileobj=buffer, mode="w"):
            pass

