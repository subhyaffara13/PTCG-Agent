
def _zip_descr(seqarrays, flatten=False):
    """
    Combine the dtype description of a series of arrays.

    Parameters
    ----------
    seqarrays : sequence of arrays
        Sequence of arrays
    flatten : {boolean}, optional
        Whether to collapse nested descriptions.
    """
    return _zip_dtype(seqarrays, flatten=flatten).descr

