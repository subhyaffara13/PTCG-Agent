
def _nanminmax(meth, fill_value_typ):
    @bottleneck_switch(name=f"nan{meth}")
    @_datetimelike_compat
    def reduction(
        values: np.ndarray,
        *,
        axis: AxisInt | None = None,
        skipna: bool = True,
        mask: npt.NDArray[np.bool_] | None = None,
    ):
        if values.size == 0:
            return _na_for_min_count(values, axis)

        dtype = values.dtype
        values, mask = _get_values(
            values, skipna, fill_value_typ=fill_value_typ, mask=mask
        )
        result = getattr(values, meth)(axis)
        result = _maybe_null_out(
            result, axis, mask, values.shape, datetimelike=dtype.kind in "mM"
        )
        return result

    return reduction

