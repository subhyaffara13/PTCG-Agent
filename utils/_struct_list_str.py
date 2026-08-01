
def _struct_list_str(dtype):
    items = []
    for name in dtype.names:
        fld_dtype, fld_offset, title = _unpack_field(*dtype.fields[name])

        item = "("
        if title is not None:
            item += f"({title!r}, {name!r}), "
        else:
            item += f"{name!r}, "
        # Special case subarray handling here
        if fld_dtype.subdtype is not None:
            base, shape = fld_dtype.subdtype
            item += f"{_construction_repr(base, short=True)}, {shape}"
        else:
            item += _construction_repr(fld_dtype, short=True)

        item += ")"
        items.append(item)

    return "[" + ", ".join(items) + "]"

