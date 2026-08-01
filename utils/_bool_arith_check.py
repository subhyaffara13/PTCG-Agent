
def _bool_arith_check(op, a: np.ndarray, b) -> None:
    """
    In contrast to numpy, pandas raises an error for certain operations
    with booleans.
    """
    if op in _BOOL_OP_NOT_ALLOWED:
        if a.dtype.kind == "b" and (is_bool_dtype(b) or lib.is_bool(b)):
            op_name = op.__name__.strip("_").lstrip("r")
            raise NotImplementedError(
                f"operator '{op_name}' not implemented for bool dtypes"
            )

