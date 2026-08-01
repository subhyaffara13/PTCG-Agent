
def _deprecate_dtypes(func_name, *arrays):
    """
    A temporary helper for deprecating non-LAPACK dtypes.
    """
    # XXX Once the deprecation expires, merge
    # linalg/lapack.py::_normalize_lapack_dtype and _normalize_lapack_dtype1, and
    # simplify _ensure_dtype_cdsz
    for a in arrays:
        if a is None:
            continue
        if a.dtype.char not in np.typecodes['AllInteger'] + 'fdFD':
            msg = (f"Calling {func_name} with arguments of dtype={a.dtype} "
                   f"({a.dtype.char = }) is deprecated in SciPy 1.18.0 and "
                    "will be removed in SciPy 1.20.0. Please cast array inputs to "
                    "one of np.float{32,64} or np.complex{64,128} manually."
            )
            import warnings
            warnings.warn(msg, category=DeprecationWarning, stacklevel=3)
            return

