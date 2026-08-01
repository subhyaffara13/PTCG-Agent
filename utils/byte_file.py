
def byte_file():
    _file_handle = io.BytesIO()
    yield _file_handle
    _file_handle.seek(0)

