
def temp_file(tmp_path):
    """
    Generate a unique file for testing use. See link for removal policy.
    https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html#the-default-base-temporary-directory
    """
    file_path = tmp_path / str(uuid.uuid4())
    file_path.touch()
    return file_path


def temp_file(tmp_path):
    return tmp_path / 'file'

