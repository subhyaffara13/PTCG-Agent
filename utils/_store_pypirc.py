
def _store_pypirc(index):
    PyPIRCFile().update(index.username, index.password)

