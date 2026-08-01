
def to_writeable(source):
    ''' Convert input object ``source`` to something we can write

    Parameters
    ----------
    source : object

    Returns
    -------
    arr : None or ndarray or EmptyStructMarker
        If `source` cannot be converted to something we can write to a matfile,
        return None.  If `source` is equivalent to an empty dictionary, return
        ``EmptyStructMarker``.  Otherwise return `source` converted to an
        ndarray with contents for writing to matfile.
    '''
    if isinstance(source, np.ndarray):
        return source
    if source is None:
        return None
    if hasattr(source, "__array__"):
        return np.asarray(source)
    # Objects that implement mappings
    is_mapping = (hasattr(source, 'keys') and hasattr(source, 'values') and
                  hasattr(source, 'items'))
    # Objects that don't implement mappings, but do have dicts
    if isinstance(source, np.generic):
        # NumPy scalars are never mappings
        pass
    elif not is_mapping and hasattr(source, '__dict__'):
        source = {key: value for key, value in source.__dict__.items()
                      if not key.startswith('_')}
        is_mapping = True
    if is_mapping:
        dtype = []
        values = []
        for field, value in source.items():
            if isinstance(field, str):
                if field[0] not in '_0123456789':
                    dtype.append((str(field), object))
                    values.append(value)
                else:
                    msg = (f"Starting field name with a underscore "
                           f"or a digit ({field}) is ignored")
                    warnings.warn(msg, MatWriteWarning, stacklevel=2)
        if dtype:
            return np.array([tuple(values)], dtype)
        else:
            return EmptyStructMarker
    # Next try and convert to an array
    try:
        narr = np.asanyarray(source)
    except ValueError:
        narr = np.asanyarray(source, dtype=object)
    if narr.dtype.type in (object, np.object_) and \
       narr.shape == () and narr == source:
        # No interesting conversion possible
        return None
    return narr

