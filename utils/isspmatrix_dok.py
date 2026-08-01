
def isspmatrix_dok(x):
    """Is `x` of dok_array type?

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
        object to check for being a dok matrix

    Returns
    -------
    bool
        True if `x` is a dok matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import dok_array, dok_matrix, coo_matrix, isspmatrix_dok
    >>> isspmatrix_dok(dok_matrix([[5]]))
    True
    >>> isspmatrix_dok(dok_array([[5]]))
    False
    >>> isspmatrix_dok(coo_matrix([[5]]))
    False
    """
    return isinstance(x, dok_matrix)

