
def _struct_dict_str(dtype, includealignedflag):
    # unpack the fields dictionary into ls
    names = dtype.names
    fld_dtypes = []
    offsets = []
    titles = []
    for name in names:
        fld_dtype, offset, title = _unpack_field(*dtype.fields[name])
        fld_dtypes.append(fld_dtype)
        offsets.append(offset)
        titles.append(title)

    # Build up a string to make the dictionary

    if np._core.arrayprint._get_legacy_print_mode() <= 121:
        colon = ":"
        fieldsep = ","
    else:
        colon = ": "
        fieldsep = ", "

    # First, the names
    ret = f"{{'names'{colon}["
    ret += fieldsep.join(repr(name) for name in names)

    # Second, the formats
    ret += f"], 'formats'{colon}["
    ret += fieldsep.join(
        _construction_repr(fld_dtype, short=True) for fld_dtype in fld_dtypes)

    # Third, the offsets
    ret += f"], 'offsets'{colon}["
    ret += fieldsep.join(f"{offset}" for offset in offsets)

    # Fourth, the titles
    if any(title is not None for title in titles):
        ret += f"], 'titles'{colon}["
        ret += fieldsep.join(repr(title) for title in titles)

    # Fifth, the itemsize
    ret += f"], 'itemsize'{colon}{dtype.itemsize}"

    if (includealignedflag and dtype.isalignedstruct):
        # Finally, the aligned flag
        ret += f", 'aligned'{colon}True}}"
    else:
        ret += "}"

    return ret

