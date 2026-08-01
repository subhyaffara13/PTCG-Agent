
def _all_gather_is_async(x, axis_name, *, axis_index_groups=None, axis=0,
                         tiled=False, to: str = 'varying', is_async: bool =
                         False):
  _allowed_ag_to = {'varying', 'reduced', 'invarying'}
  if to not in _allowed_ag_to:
    raise ValueError(
        "Got unexpected `to` value for `jax.lax.all_gather`. Allowed `to`"
        f" values are: {_allowed_ag_to}")
  if to == 'varying':
    return _all_gather(x, axis_name, axis_index_groups=axis_index_groups,
                       axis=axis, tiled=tiled, is_async=is_async)
  elif to == 'invarying':
    if axis_index_groups is not None:
      raise NotImplementedError
    return all_gather_invariant(x, axis_name, axis=axis, tiled=tiled)
  else:
    assert to == 'reduced'
    if axis_index_groups is not None:
      raise NotImplementedError
    return all_gather_reduced(x, axis_name, axis=axis, tiled=tiled,
                              is_async=is_async)

