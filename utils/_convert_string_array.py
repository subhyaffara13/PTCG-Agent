
def _convert_string_array(data: np.ndarray, encoding: str, errors: str) -> np.ndarray:
    """
    Take a string-like that is object dtype and coerce to a fixed size string type.

    Parameters
    ----------
    data : np.ndarray[object]
    encoding : str
    errors : str
        Handler for encoding errors.

    Returns
    -------
    np.ndarray[fixed-length-string]
    """
    # encode if needed
    if len(data):
        data = (
            Series(data.ravel(), copy=False, dtype="object")
            .str.encode(encoding, errors)
            ._values.reshape(data.shape)
        )

    # create the sized dtype
    ensured = ensure_object(data.ravel())
    itemsize = max(1, libwriters.max_len_string_array(ensured))

    data = np.asarray(data, dtype=f"S{itemsize}")
    return data

