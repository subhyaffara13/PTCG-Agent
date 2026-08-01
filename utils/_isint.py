
def _isint(x):
    if HAS_NUMPY:
        return isinstance(x, (int, np.integer))  # pyrefly: ignore [missing-attribute]
    else:
        return isinstance(x, int)

