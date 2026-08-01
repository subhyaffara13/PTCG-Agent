
def _require_listlike(level, arr, arrname: str):
    """
    Ensure that level is either None or listlike, and arr is list-of-listlike.
    """
    if level is not None and not is_list_like(level):
        if not is_list_like(arr):
            raise TypeError(f"{arrname} must be list-like")
        if len(arr) > 0 and is_list_like(arr[0]):
            raise TypeError(f"{arrname} must be list-like")
        level = [level]
        arr = [arr]
    elif level is None or is_list_like(level):
        if not is_list_like(arr) or not is_list_like(arr[0]):
            raise TypeError(f"{arrname} must be list of lists-like")
    return level, arr

