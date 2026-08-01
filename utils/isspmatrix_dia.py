
def isspmatrix_dia(x):
    """Is `x` of dia_matrix type?

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
        object to check for being a dia matrix

    Returns
    -------
    bool
        True if `x` is a dia matrix, False otherwise

    Examples
    --------
    >>> from scipy.sparse import dia_array, dia_matrix, coo_matrix, isspmatrix_dia
    >>> isspmatrix_dia(dia_matrix([[5]]))
    True
    >>> isspmatrix_dia(dia_array([[5]]))
    False
    >>> isspmatrix_dia(coo_matrix([[5]]))
    False
    """
    return isinstance(x, dia_matrix)

