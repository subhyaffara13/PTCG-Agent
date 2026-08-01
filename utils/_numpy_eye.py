
def _numpy_eye(n):
    """numpy version of complex eye."""
    if not np:
        raise ImportError
    return np.array(np.eye(n, dtype='complex'))

