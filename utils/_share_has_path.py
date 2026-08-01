
def _share_has_path(path):
    parts = path.count("/")
    if path.endswith("/"):
        return parts > 2
    return parts > 1

