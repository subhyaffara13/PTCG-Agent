
def isspmatrix_bsr(x):
    """Is `x` of a bsr_matrix type?

    .. warning::

       SciPy sparse is shifting from a sparse matrix interface to a sparse
       array interface. In the next few releases we expect to deprecate the
       sparse matrix interface. For documentation of the matrix
       interface, see the :ref:`spmatrix interface docs <spmatrix_api>`.
       For guidance on converting existing code to sparse arrays, see
       :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.

    Parameters
    ----------
    x
        object to check for being a bsr matrix

    Returns
    -------
    bool
        True if `x` is a bsr matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import bsr_array, bsr_matrix, csr_matrix, isspmatrix_bsr
    >>> isspmatrix_bsr(bsr_matrix([[5]]))
    True
    >>> isspmatrix_bsr(bsr_array([[5]]))
    False
    >>> isspmatrix_bsr(csr_matrix([[5]]))
    False
    """
    return isinstance(x, bsr_matrix)

