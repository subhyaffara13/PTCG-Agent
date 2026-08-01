
def _unconvert_string_array(
    data: np.ndarray, nan_rep, encoding: str, errors: str
) -> np.ndarray:
    """
    Inverse of _convert_string_array.

    Parameters
    ----------
    data : np.ndarray[fixed-length-string]
    nan_rep : the storage repr of NaN
    encoding : str
    errors : str
        Handler for encoding errors.

    Returns
    -------
    np.ndarray[object]
        Decoded data.
    """
    shape = data.shape
    data = np.asarray(data.ravel(), dtype=object)

    if len(data):
        itemsize = libwriters.max_len_string_array(ensure_object(data))
        dtype = f"U{itemsize}"

        if isinstance(data[0], bytes):
            ser = Series(data, copy=False).str.decode(
                encoding, errors=errors, dtype="object"
            )
            data = ser.to_numpy()
            data.flags.writeable = True
        else:
            data = data.astype(dtype, copy=False).astype(object, copy=False)

    if nan_rep is None:
        nan_rep = "nan"

    libwriters.string_array_replace_from_nan_rep(data, nan_rep)
    return data.reshape(shape)

