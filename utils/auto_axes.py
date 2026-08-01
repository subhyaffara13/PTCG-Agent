
def auto_axes(f=None, /, *, axes: str | tuple[str, ...] | None = None,
              out_sharding=None):
  kwargs = dict(axes_=axes, out_sharding=out_sharding)
  if f is None:
    return lambda g: _auto_axes(g, **kwargs)
  return _auto_axes(f, **kwargs)

