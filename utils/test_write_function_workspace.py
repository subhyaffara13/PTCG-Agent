
def test_write_function_workspace():
    """Test that we can write function workspace to a MAT-file"""

    workspace = "This is not the actual workspace contents. Just a test"
    stream = BytesIO()
    savemat(stream, {'__function_workspace__': workspace})
    stream.seek(0)
    data = loadmat(stream)
    assert "__function_workspace__" in data

