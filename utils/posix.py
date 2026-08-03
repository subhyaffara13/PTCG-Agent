import os

def posix(path):
    if not isinstance(path, str):
        return path.replace(os.sep.encode('ascii'), b'/')
    else:
        return path.replace(os.sep, '/')


def posix(path):
    """Normalize paths using forward slash to work also on Windows."""
    new_path = posixpath.join(*path.split(os.path.sep))
    if path.startswith("/"):
        # The above transformation loses absolute paths
        new_path = "/" + new_path
    elif path.startswith(r"\\"):
        # The above transformation loses leading slashes of UNC path mounts
        new_path = "//" + new_path
    return new_path

