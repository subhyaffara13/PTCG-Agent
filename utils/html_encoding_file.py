
def html_encoding_file(request, datapath):
    """Parametrized fixture for HTML encoding test filenames."""
    return datapath("io", "data", "html_encoding", request.param)

