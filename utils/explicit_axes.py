
def explicit_axes(f=None, /, *, axes: str | tuple[str, ...] | None = None,
                  in_sharding=None):
  kwargs = dict(axes=axes, in_sharding=in_sharding)
  if f is None:
    return lambda g: _explicit_axes(g, **kwargs)
  return _explicit_axes(f, **kwargs)

