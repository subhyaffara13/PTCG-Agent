import uuid

def temp_h5_path(tmp_path):
    """Fixture for HDF5 path"""
    file_path = tmp_path / f"{uuid.uuid4()}.h5"
    file_path.touch()
    return file_path

