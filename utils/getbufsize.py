
def getbufsize():
    """
    Return the size of the buffer used in ufuncs.

    Returns
    -------
    getbufsize : int
        Size of ufunc buffer in bytes.

    Notes
    -----

    **Concurrency note:** see :doc:`/reference/routines.err`


    Examples
    --------
    >>> import numpy as np
    >>> np.getbufsize()
    8192

    """
    return _get_extobj_dict()["bufsize"]

