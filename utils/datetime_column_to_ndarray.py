from typing import Any

def datetime_column_to_ndarray(col: Column) -> tuple[np.ndarray | pd.Series, Any]:
    """
    Convert a column holding DateTime data to a NumPy array.

    Parameters
    ----------
    col : Column

    Returns
    -------
    tuple
        Tuple of np.ndarray holding the data and the memory owner object
        that keeps the memory alive.
    """
    buffers = col.get_buffers()

    _, col_bit_width, format_str, _ = col.dtype
    dbuf, _ = buffers["data"]
    # Consider dtype being `uint` to get number of units passed since the 01.01.1970

    data = buffer_to_ndarray(
        dbuf,
        (
            DtypeKind.INT,
            col_bit_width,
            getattr(ArrowCTypes, f"INT{col_bit_width}"),
            Endianness.NATIVE,
        ),
        offset=col.offset,
        length=col.size(),
    )

    data = parse_datetime_format_str(format_str, data)  # type: ignore[assignment]
    data = set_nulls(data, col, buffers["validity"])
    return data, buffers

