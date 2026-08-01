
def is_valid_pylock_filename(filename: str) -> bool:
    if _is_url(filename):
        path = Path(urlsplit(filename).path.rpartition("/")[-1])
    else:
        path = Path(filename)
    return is_valid_pylock_path(path)

