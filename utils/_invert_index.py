
def _invert_index(idx):
    """Helper function to invert an index array."""
    inv = np.zeros_like(idx)
    inv[idx] = np.arange(len(idx))
    return inv

