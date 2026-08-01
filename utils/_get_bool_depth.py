
def _get_bool_depth(s):
    """Returns the depth of a boolean sequence/tensor"""
    if isinstance(s, bool):
        return True, 0
    if isinstance(s, torch.Tensor) and s.dtype == torch.bool:
        return True, s.ndim
    if not (isinstance(s, Sequence) and s and s[0] != s):
        return False, 0
    is_bool, depth = _get_bool_depth(s[0])
    return is_bool, depth + 1

