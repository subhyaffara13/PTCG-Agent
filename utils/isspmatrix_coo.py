
def isspmatrix_coo(x):
    """Is `x` of coo_matrix type?

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
        object to check for being a coo matrix

    Returns
    -------
    bool
        True if `x` is a coo matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import coo_array, coo_matrix, csr_matrix, isspmatrix_coo
    >>> isspmatrix_coo(coo_matrix([[5]]))
    True
    >>> isspmatrix_coo(coo_array([[5]]))
    False
    >>> isspmatrix_coo(csr_matrix([[5]]))
    False
    """
    return isinstance(x, coo_matrix)

