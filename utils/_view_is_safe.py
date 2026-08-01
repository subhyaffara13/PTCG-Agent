
def _view_is_safe(oldtype, newtype):
    """ Checks safety of a view involving object arrays, for example when
    doing::

        np.zeros(10, dtype=oldtype).view(newtype)

    Parameters
    ----------
    oldtype : data-type
        Data type of original ndarray
    newtype : data-type
        Data type of the view

    Raises
    ------
    TypeError
        If the new type is incompatible with the old type.

    """

    # more precise than ``oldtype == newtype``: e.g. dtype((np.record, 'i4,i4'))
    # views safely as dtype((np.void, 'i4,i4')), while two equal StringDType
    # instances with separate allocators do not
    if _is_view_safe_cast(oldtype, newtype):
        return

    if newtype.hasobject or oldtype.hasobject:
        raise TypeError("Cannot change data-type for array of references.")
    return

