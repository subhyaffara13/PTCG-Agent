
def _get_na_rep(dtype: DtypeObj) -> str:
    if isinstance(dtype, ExtensionDtype):
        return f"{dtype.na_value}"
    else:
        dtype_type = dtype.type

    return {np.datetime64: "NaT", np.timedelta64: "NaT"}.get(dtype_type, "NaN")

