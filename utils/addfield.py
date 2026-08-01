
def addfield(mrecord, newfield, newfieldname=None):
    """Adds a new field to the masked record array

    Uses `newfield` as data and `newfieldname` as name. If `newfieldname`
    is None, the new field name is set to 'fi', where `i` is the number of
    existing fields.

    """
    _data = mrecord._data
    _mask = mrecord._mask
    if newfieldname is None or newfieldname in reserved_fields:
        newfieldname = f'f{len(_data.dtype)}'
    newfield = ma.array(newfield)
    # Get the new data.
    # Create a new empty recarray
    newdtype = np.dtype(_data.dtype.descr + [(newfieldname, newfield.dtype)])
    newdata = np.recarray(_data.shape, newdtype)
    # Add the existing field
    [newdata.setfield(_data.getfield(*f), *f)
     for f in _data.dtype.fields.values()]
    # Add the new field
    newdata.setfield(newfield._data, *newdata.dtype.fields[newfieldname])
    newdata = newdata.view(MaskedRecords)
    # Get the new mask
    # Create a new empty recarray
    newmdtype = np.dtype([(n, np.bool) for n in newdtype.names])
    newmask = np.recarray(_data.shape, newmdtype)
    # Add the old masks
    [newmask.setfield(_mask.getfield(*f), *f)
     for f in _mask.dtype.fields.values()]
    # Add the mask of the new field
    newmask.setfield(ma.getmaskarray(newfield),
                     *newmask.dtype.fields[newfieldname])
    newdata._mask = newmask
    return newdata

