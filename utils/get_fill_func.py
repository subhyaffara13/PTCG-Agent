
def get_fill_func(method, ndim: int = 1):
    method = clean_fill_method(method)
    if ndim == 1:
        return _fill_methods[method]
    return {"pad": _pad_2d, "backfill": _backfill_2d}[method]

