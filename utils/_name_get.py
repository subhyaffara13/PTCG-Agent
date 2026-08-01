
def _name_get(dtype):
    # provides dtype.name.__get__, documented as returning a "bit name"

    if dtype.isbuiltin == 2:
        # user dtypes don't promise to do anything special
        return dtype.type.__name__

    if not type(dtype)._legacy:
        name = type(dtype).__name__

    elif issubclass(dtype.type, np.void):
        # historically, void subclasses preserve their name, eg `record64`
        name = dtype.type.__name__
    else:
        name = _kind_name(dtype)

    # append bit counts
    if _name_includes_bit_suffix(dtype):
        name += f"{dtype.itemsize * 8}"

    # append metadata to datetimes
    if dtype.type in (np.datetime64, np.timedelta64):
        name += _datetime_metadata_str(dtype)

    return name

