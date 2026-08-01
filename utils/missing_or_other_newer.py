
def missing_or_other_newer(path, other_path, cwd=None):
    """
    Investigate if path is non-existent or older than provided reference
    path.

    Parameters
    ==========
    path: string
        path to path which might be missing or too old
    other_path: string
        reference path
    cwd: string
        working directory (root of relative paths)

    Returns
    =======
    True if path is older or missing.
    """
    cwd = cwd or '.'
    path = get_abspath(path, cwd=cwd)
    other_path = get_abspath(other_path, cwd=cwd)
    if not os.path.exists(path):
        return True
    if os.path.getmtime(other_path) - 1e-6 >= os.path.getmtime(path):
        # 1e-6 is needed because http://stackoverflow.com/questions/17086426/
        return True
    return False

