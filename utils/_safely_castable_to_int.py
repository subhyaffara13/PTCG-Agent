
def _safely_castable_to_int(dt):
    """Test whether the NumPy data type `dt` can be safely cast to an int."""
    int_size = np.dtype(int).itemsize
    safe = ((np.issubdtype(dt, np.signedinteger) and dt.itemsize <= int_size) or
            (np.issubdtype(dt, np.unsignedinteger) and dt.itemsize < int_size))
    return safe

