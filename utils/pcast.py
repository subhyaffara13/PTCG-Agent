
def pcast(x, axis_name, *, to: str):
  if isinstance(axis_name, (set, frozenset)):
    raise TypeError(f"{axis_name=} must be a tuple or a str. Got {axis_name}")
  axes = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  if not axis_name:
    return x

  if to not in _allowed_pcast_to:
    raise ValueError(
        "Got unexpected `to` value. Allowed `to` values are:"
        f" {_allowed_pcast_to}")

  def bind(leaf):
    from_ = _get_from(core.typeof(leaf), axes, 'jax.lax.pcast')
    func = _pcast_funcs.get((from_, to), None)
    if func is None:
      raise ValueError(f"Unsupported pcast from={from_}, {to=}")
    return func(leaf, axes)
  return tree_util.tree_map(bind, x)

