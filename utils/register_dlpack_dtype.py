
def register_dlpack_dtype(dlpack_key, dtype, /):
    """
    Register a NumPy dtype for a DLPack ``(code, bits)`` pair so that
    `numpy.from_dlpack` can import it and ``ndarray.__dlpack__`` can export
    it.  Built-in dtype mappings take priority on import.

    If you think a conflict is possible but unproblematic you may wrap this
    into a try/except block as NumPy will raise an error if another DType
    is already registered for the same (code, bits) pair.
    While an error is raised, the export is registered even on error.

    Registering an identical (not equal) dtype multiple times is allowed but
    normally registration should happen at import time.

    .. warning::
        It is the responsibility of the registering user to ensure that the
        mapping is valid.

    .. note::
        This function was added primarily for ``ml_dtypes`` and may be
        replaced with a different mechanism in the future.  It is intended
        to be used by authors of user-defined dtypes and not end-users.

    Parameters
    ----------
    dlpack_key : tuple of int
        ``(dl_dtype_code, dl_bits)`` matching the DLPack ``DLDataType``,
        lanes is assumed to be always 1, currently.
    dtype : dtype
        A NumPy dtype instance.

    Raises
    ------
    ValueError : If a conflicting registration was already done.

    See Also
    --------
    numpy.from_dlpack

    """
    # Deferred to avoid circular import.
    from numpy._core._multiarray_umath import _register_dlpack_dtype

    return _register_dlpack_dtype(dlpack_key, dtype)

