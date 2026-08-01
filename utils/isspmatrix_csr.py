
def isspmatrix_csr(x):
    """Is `x` of csr_matrix type?

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
        object to check for being a csr matrix

    Returns
    -------
    bool
        True if `x` is a csr matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import csr_array, csr_matrix, coo_matrix, isspmatrix_csr
    >>> isspmatrix_csr(csr_matrix([[5]]))
    True
    >>> isspmatrix_csr(csr_array([[5]]))
    False
    >>> isspmatrix_csr(coo_matrix([[5]]))
    False
    """
    return isinstance(x, csr_matrix)

