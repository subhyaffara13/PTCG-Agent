
def isspmatrix(x):
    """Is `x` of a sparse matrix type?

    .. warning::

        scipy.sparse is switching to the sparse array interface.

        The ``isspmatrix`` function returns ``False`` for sparse arrays.
        It will remain after the switch to sparse arrays (sparray).
        So this is a future proof way to check for sparray vs spmatrix.
        If you just want to check for sparse, use ``issparse(A)``.
        For more general information about sparrays, see
        :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.
        The switch to sparse arrays will occur no earlier than v1.21.

    Parameters
    ----------
    x
        object to check for being a sparse matrix

    Returns
    -------
    bool
        True if `x` is a sparse matrix, False otherwise

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csr_array, csr_matrix, isspmatrix
    >>> isspmatrix(csr_matrix([[5]]))
    True
    >>> isspmatrix(csr_array([[5]]))
    False
    >>> isspmatrix(np.array([[5]]))
    False
    >>> isspmatrix(5)
    False
    """
    return isinstance(x, spmatrix)

