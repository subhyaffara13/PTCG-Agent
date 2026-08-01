
def mlarr(*args, **kwargs):
    """Convenience function to return matlab-compatible 2-D array."""
    arr = np.array(*args, **kwargs)
    arr = arr.reshape(matdims(arr))
    return arr

