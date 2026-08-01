
def get_fieldstructure(adtype, lastname=None, parents=None,):
    """
    Returns a dictionary with fields indexing lists of their parent fields.

    This function is used to simplify access to fields nested in other fields.

    Parameters
    ----------
    adtype : np.dtype
        Input datatype
    lastname : optional
        Last processed field name (used internally during recursion).
    parents : dictionary
        Dictionary of parent fields (used internally during recursion).

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.lib import recfunctions as rfn
    >>> ndtype =  np.dtype([('A', int),
    ...                     ('B', [('BA', int),
    ...                            ('BB', [('BBA', int), ('BBB', int)])])])
    >>> rfn.get_fieldstructure(ndtype)
    ... # XXX: possible regression, order of BBA and BBB is swapped
    {'A': [], 'B': [], 'BA': ['B'], 'BB': ['B'], 'BBA': ['B', 'BB'], 'BBB': ['B', 'BB']}

    """
    if parents is None:
        parents = {}
    names = adtype.names
    for name in names:
        current = adtype[name]
        if current.names is not None:
            if lastname:
                parents[name] = [lastname, ]
            else:
                parents[name] = []
            parents.update(get_fieldstructure(current, name, parents))
        else:
            lastparent = list(parents.get(lastname, []) or [])
            if lastparent:
                lastparent.append(lastname)
            elif lastname:
                lastparent = [lastname, ]
            parents[name] = lastparent or []
    return parents

