
def isspmatrix_lil(x):
    """Is `x` of lil_matrix type?

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
        object to check for being a lil matrix

    Returns
    -------
    bool
        True if `x` is a lil matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import lil_array, lil_matrix, coo_matrix, isspmatrix_lil
    >>> isspmatrix_lil(lil_matrix([[5]]))
    True
    >>> isspmatrix_lil(lil_array([[5]]))
    False
    >>> isspmatrix_lil(coo_matrix([[5]]))
    False
    """
    return isinstance(x, lil_matrix)

