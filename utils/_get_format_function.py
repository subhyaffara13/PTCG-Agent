
def _get_format_function(data, **options):
    """
    find the right formatting function for the dtype_
    """
    dtype_ = data.dtype
    dtypeobj = dtype_.type
    formatdict = _get_formatdict(data, **options)

    if dtypeobj is None:
        return formatdict["numpystr"]()
    elif (getattr(dtypeobj, "__module__", None) != "numpy"
            and not issubclass(dtypeobj, str)):
        # Use `str()` as a default format for non-NumPy dtypes. This should be
        # improved.  We use `str` assuming that `repr` is likely to duplicate
        # information that is contained in the dtype.
        # (Do this early, because e.g. quaddtype subclasses floating.)
        return formatdict['void']()
    elif issubclass(dtypeobj, _nt.bool):
        return formatdict['bool']()
    elif issubclass(dtypeobj, _nt.integer):
        if issubclass(dtypeobj, _nt.timedelta64):
            return formatdict['timedelta']()
        else:
            return formatdict['int']()
    elif issubclass(dtypeobj, _nt.floating):
        if issubclass(dtypeobj, _nt.longdouble):
            return formatdict['longfloat']()
        else:
            return formatdict['float']()
    elif issubclass(dtypeobj, _nt.complexfloating):
        if issubclass(dtypeobj, _nt.clongdouble):
            return formatdict['longcomplexfloat']()
        else:
            return formatdict['complexfloat']()
    elif issubclass(dtypeobj, (_nt.str_, _nt.bytes_)):
        return formatdict['numpystr']()
    elif issubclass(dtypeobj, _nt.datetime64):
        return formatdict['datetime']()
    elif issubclass(dtypeobj, _nt.object_):
        return formatdict['object']()
    elif issubclass(dtypeobj, _nt.void):
        if dtype_.names is not None:
            return StructuredVoidFormat.from_data(data, **options)
        else:
            return formatdict['void']()
    else:
        return formatdict['numpystr']()

