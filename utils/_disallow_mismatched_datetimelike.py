
def _disallow_mismatched_datetimelike(value, dtype: DtypeObj) -> None:
    """
    numpy allows np.array(dt64values, dtype="timedelta64[ns]") and
    vice-versa, but we do not want to allow this, so we need to
    check explicitly
    """
    vdtype = getattr(value, "dtype", None)
    if vdtype is None:
        return
    elif (vdtype.kind == "m" and dtype.kind == "M") or (
        vdtype.kind == "M" and dtype.kind == "m"
    ):
        raise TypeError(f"Cannot cast {value!r} to {dtype}")

