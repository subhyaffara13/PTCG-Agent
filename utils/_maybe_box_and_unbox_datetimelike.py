
def _maybe_box_and_unbox_datetimelike(value: Scalar, dtype: DtypeObj):
    # Caller is responsible for checking dtype.kind in "mM"

    if isinstance(value, dt.datetime):
        # we dont want to box dt64, in particular datetime64("NaT")
        value = maybe_box_datetimelike(value, dtype)

    return _maybe_unbox_datetimelike(value, dtype)

