
def _struct_str(dtype, include_align):
    # The list str representation can't include the 'align=' flag,
    # so if it is requested and the struct has the aligned flag set,
    # we must use the dict str instead.
    if not (include_align and dtype.isalignedstruct) and _is_packed(dtype):
        sub = _struct_list_str(dtype)

    else:
        sub = _struct_dict_str(dtype, include_align)

    # If the data type isn't the default, void, show it
    if dtype.type != np.void:
        return f"({dtype.type.__module__}.{dtype.type.__name__}, {sub})"
    else:
        return sub

