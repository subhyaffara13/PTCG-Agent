
def open_temp_file():
    file = tempfile.NamedTemporaryFile(delete=False)
    filename = file.name
    return file, filename

