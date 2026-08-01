
def to_uri(file_path):
    pure_path = pathlib.PurePath(file_path)
    if pure_path.is_absolute():
        return pure_path.as_uri()
    else:
        # Replace backslashes with slashes.
        posix_path = pure_path.as_posix()
        # %-encode special characters.
        return urlparse.quote(posix_path)

