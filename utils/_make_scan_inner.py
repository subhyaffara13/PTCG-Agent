
def _make_scan_inner(x, *, axis, dtype):
    if dtype is not None:
        x = to_dtype(x, dtype)
    axis = _validate_dim(x, axis)

    return dict(
        device=x.get_device(),
        dtypes=(x.get_dtype(),),
        inner_fns=(x.make_loader(),),
        size=x.get_size(),
        axis=axis,
    )

