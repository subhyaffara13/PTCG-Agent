
def legacy_path(path: str | os.PathLike[str]) -> LEGACY_PATH:
    """Internal wrapper to prepare lazy proxies for legacy_path instances"""
    return LEGACY_PATH(path)

