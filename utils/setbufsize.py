
def setbufsize(size):
    """
    Set the size of the buffer used in ufuncs.

    .. versionchanged:: 2.0
        The scope of setting the buffer is tied to the `numpy.errstate`
        context.  Exiting a ``with errstate():`` will also restore the bufsize.

    Parameters
    ----------
    size : int
        Size of buffer.

    Returns
    -------
    bufsize : int
        Previous size of ufunc buffer in bytes.

    Notes
    -----
    **Concurrency note:** see :doc:`/reference/routines.err`

    Examples
    --------
    When exiting a `numpy.errstate` context manager the bufsize is restored:

    >>> import numpy as np
    >>> with np.errstate():
    ...     np.setbufsize(4096)
    ...     print(np.getbufsize())
    ...
    8192
    4096
    >>> np.getbufsize()
    8192

    """
    if size < 0:
        raise ValueError("buffer size must be non-negative")
    old = _get_extobj_dict()["bufsize"]
    extobj = _make_extobj(bufsize=size)
    _extobj_contextvar.set(extobj)
    return old

