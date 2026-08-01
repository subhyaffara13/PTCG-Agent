
def _import_numpy():
    """Make sure `numpy` is installed on the machine."""
    if not is_numpy_available():
        raise ImportError("Please install numpy to use deal with embeddings (`pip install numpy`).")
    import numpy

    return numpy

