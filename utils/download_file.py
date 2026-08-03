import os

def download_file(url, binary=True):
    from urllib.parse import urlsplit
    from urllib import request, error

    filename = os.path.basename(urlsplit(url)[2])
    data_dir = get_writable_path(os.path.join(os.path.dirname(__file__), 'data'))
    path = os.path.join(data_dir, filename)

    if os.path.exists(path):
        return path
    try:
        with request.urlopen(url, timeout=15) as f1, open(path, 'wb' if binary else 'w') as f2:
            data = f1.read()
            f2.write(data)
        return path
    except error.URLError as e:
        msg = f"could not download test file '{url}'"
        warnings.warn(msg, RuntimeWarning, stacklevel=2)
        raise unittest.SkipTest(msg) from e

