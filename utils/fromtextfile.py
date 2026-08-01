
def fromtextfile(fname, delimiter=None, commentchar='#', missingchar='',
                 varnames=None, vartypes=None):
    """
    Creates a mrecarray from data stored in the file `filename`.

    Parameters
    ----------
    fname : {file name/handle}
        Handle of an opened file.
    delimiter : {None, string}, optional
        Alphanumeric character used to separate columns in the file.
        If None, any (group of) white spacestring(s) will be used.
    commentchar : {'#', string}, optional
        Alphanumeric character used to mark the start of a comment.
    missingchar : {'', string}, optional
        String indicating missing data, and used to create the masks.
    varnames : {None, sequence}, optional
        Sequence of the variable names. If None, a list will be created from
        the first non empty line of the file.
    vartypes : {None, sequence}, optional
        Sequence of the variables dtypes. If None, it will be estimated from
        the first non-commented line.


    Ultra simple: the varnames are in the header, one line"""

    # Try to open the file.
    ftext = openfile(fname)

    # Get the first non-empty line as the varnames
    while True:
        line = ftext.readline()
        firstline = line[:line.find(commentchar)].strip()
        _varnames = firstline.split(delimiter)
        if len(_varnames) > 1:
            break
    if varnames is None:
        varnames = _varnames

    # Get the data.
    _variables = ma.masked_array([line.strip().split(delimiter) for line in ftext
                                 if line[0] != commentchar and len(line) > 1])
    (_, nfields) = _variables.shape
    ftext.close()

    # Try to guess the dtype.
    if vartypes is None:
        vartypes = _guessvartypes(_variables[0])
    else:
        vartypes = [np.dtype(v) for v in vartypes]
        if len(vartypes) != nfields:
            msg = f"Attempting to {len(vartypes)} dtypes for {nfields} fields!"
            msg += " Reverting to default."
            warnings.warn(msg, stacklevel=2)
            vartypes = _guessvartypes(_variables[0])

    # Construct the descriptor.
    mdescr = list(zip(varnames, vartypes))
    mfillv = [ma.default_fill_value(f) for f in vartypes]

    # Get the data and the mask.
    # We just need a list of masked_arrays. It's easier to create it like that:
    _mask = (_variables.T == missingchar)
    _datalist = [ma.masked_array(a, mask=m, dtype=t, fill_value=f)
                 for (a, m, t, f) in zip(_variables.T, _mask, vartypes, mfillv)]

    return fromarrays(_datalist, dtype=mdescr)

