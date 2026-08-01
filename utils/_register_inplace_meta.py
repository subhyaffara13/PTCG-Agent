
def _register_inplace_meta(fn):
    @wraps(fn)
    def _fn(self, *args, **kwargs):
        out = fn(self, *args, **kwargs)
        check_inplace_broadcast(self.shape, out.shape)
        return self

    inplace_name = f"{fn.__name__}_"
    _fn.__name__ = inplace_name
    _fn = register_meta(getattr(aten, inplace_name))(_fn)  # type: ignore[assignment]

    return _fn

