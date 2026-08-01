
def _load_pypirc(index):
    """
    Read the PyPI access configuration as supported by distutils.
    """
    return PyPIRCFile(url=index.url).read()

