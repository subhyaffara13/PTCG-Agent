
def string_column_to_ndarray(col: Column) -> tuple[np.ndarray, Any]:
    """
    Convert a column holding string data to a NumPy array.

    Parameters
    ----------
    col : Column

    Returns
    -------
    tuple
        Tuple of np.ndarray holding the data and the memory owner object
        that keeps the memory alive.
    """
    null_kind, sentinel_val = col.describe_null

    if null_kind not in (
        ColumnNullType.NON_NULLABLE,
        ColumnNullType.USE_BITMASK,
        ColumnNullType.USE_BYTEMASK,
    ):
        raise NotImplementedError(
            f"{null_kind} null kind is not yet supported for string columns."
        )

    buffers = col.get_buffers()

    assert buffers["offsets"], "String buffers must contain offsets"
    # Retrieve the data buffer containing the UTF-8 code units
    data_buff, _ = buffers["data"]
    # We're going to reinterpret the buffer as uint8, so make sure we can do it safely
    assert col.dtype[2] in (
        ArrowCTypes.STRING,
        ArrowCTypes.LARGE_STRING,
    )  # format_str == utf-8
    # Convert the buffers to NumPy arrays. In order to go from STRING to
    # an equivalent ndarray, we claim that the buffer is uint8 (i.e., a byte array)
    data_dtype = (
        DtypeKind.UINT,
        8,
        ArrowCTypes.UINT8,
        Endianness.NATIVE,
    )
    # Specify zero offset as we don't want to chunk the string data
    data = buffer_to_ndarray(data_buff, data_dtype, offset=0, length=data_buff.bufsize)

    # Retrieve the offsets buffer containing the index offsets demarcating
    # the beginning and the ending of each string
    offset_buff, offset_dtype = buffers["offsets"]
    # Offsets buffer contains start-stop positions of strings in the data buffer,
    # meaning that it has more elements than in the data buffer, do `col.size() + 1`
    # here to pass a proper offsets buffer size
    offsets = buffer_to_ndarray(
        offset_buff, offset_dtype, offset=col.offset, length=col.size() + 1
    )

    null_pos = None
    if null_kind in (ColumnNullType.USE_BITMASK, ColumnNullType.USE_BYTEMASK):
        validity = buffers["validity"]
        if validity is not None:
            valid_buff, valid_dtype = validity
            null_pos = buffer_to_ndarray(
                valid_buff, valid_dtype, offset=col.offset, length=col.size()
            )
            if sentinel_val == 0:
                null_pos = ~null_pos

    # Assemble the strings from the code units
    str_list: list[None | float | str] = [None] * col.size()
    for i in range(col.size()):
        # Check for missing values
        if null_pos is not None and null_pos[i]:
            str_list[i] = np.nan
            continue

        # Extract a range of code units
        units = data[offsets[i] : offsets[i + 1]]

        # Convert the list of code units to bytes
        str_bytes = bytes(units)

        # Create the string
        string = str_bytes.decode(encoding="utf-8")

        # Add to our list of strings
        str_list[i] = string

    if using_string_dtype():
        res = pd.Series(str_list, dtype="str")
    else:
        res = np.asarray(str_list, dtype="object")  # type: ignore[assignment]

    return res, buffers  # type: ignore[return-value]

