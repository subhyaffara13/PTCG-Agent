
def _get_git_hash() -> str:
    global _cached_git_hash
    if _cached_git_hash is not None:
        return _cached_git_hash
    try:
        _cached_git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
    except Exception:
        _cached_git_hash = "unknown_git"
    return _cached_git_hash

