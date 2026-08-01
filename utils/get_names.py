
def get_names(adtype):
    """
    Returns the field names of the input datatype as a tuple. Input datatype
    must have fields otherwise error is raised.

    Parameters
    ----------
    adtype : dtype
        Input datatype

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.lib import recfunctions as rfn
    >>> rfn.get_names(np.empty((1,), dtype=[('A', int)]).dtype)
    ('A',)
    >>> rfn.get_names(np.empty((1,), dtype=[('A',int), ('B', float)]).dtype)
    ('A', 'B')
    >>> adtype = np.dtype([('a', int), ('b', [('ba', int), ('bb', int)])])
    >>> rfn.get_names(adtype)
    ('a', ('b', ('ba', 'bb')))
    """
    listnames = []
    names = adtype.names
    for name in names:
        current = adtype[name]
        if current.names is not None:
            listnames.append((name, tuple(get_names(current))))
        else:
            listnames.append(name)
    return tuple(listnames)

