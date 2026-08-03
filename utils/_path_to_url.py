import os

def _path_to_url(path):
    path = os.path.normpath(os.path.abspath(path))
    url = urljoin("file:", pathname2url(path))
    return url

