
def _dtype_to_default_stata_fmt(
    dtype: np.dtype, column: Series, dta_version: int = 114, force_strl: bool = False
) -> str:
    """
    Map numpy dtype to stata's default format for this type. Not terribly
    important since users can change this in Stata. Semantics are

    object  -> "%DDs" where DD is the length of the string.  If not a string,
                raise ValueError
    float64 -> "%10.0g"
    float32 -> "%9.0g"
    int64   -> "%9.0g"
    int32   -> "%12.0g"
    int16   -> "%8.0g"
    int8    -> "%8.0g"
    strl    -> "%9s"
    """
    # TODO: Refactor to combine type with format
    # TODO: expand this to handle a default datetime format?
    if dta_version < 117:
        max_str_len = 244
    else:
        max_str_len = 2045
        if force_strl:
            return "%9s"
    if dtype.type is np.object_:
        itemsize = max_len_string_array(ensure_object(column._values))
        if itemsize > max_str_len:
            if dta_version >= 117:
                return "%9s"
            else:
                raise ValueError(excessive_string_length_error.format(column.name))
        return "%" + str(max(itemsize, 1)) + "s"
    elif dtype == np.float64:
        return "%10.0g"
    elif dtype == np.float32:
        return "%9.0g"
    elif dtype == np.int32:
        return "%12.0g"
    elif dtype in (np.int8, np.int16):
        return "%8.0g"
    else:  # pragma : no cover
        raise NotImplementedError(f"Data type {dtype} not supported.")

