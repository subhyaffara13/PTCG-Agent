
def isspmatrix_csc(x):
    """Is `x` of csc_matrix type?

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
        object to check for being a csc matrix

    Returns
    -------
    bool
        True if `x` is a csc matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import csc_array, csc_matrix, coo_matrix, isspmatrix_csc
    >>> isspmatrix_csc(csc_matrix([[5]]))
    True
    >>> isspmatrix_csc(csc_array([[5]]))
    False
    >>> isspmatrix_csc(coo_matrix([[5]]))
    False
    """
    return isinstance(x, csc_matrix)

