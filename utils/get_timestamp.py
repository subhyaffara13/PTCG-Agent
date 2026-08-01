
def get_timestamp(path: str) -> Optional[float]:
    if not os.path.isfile(path):
        return None
    return os.stat(path).st_mtime

