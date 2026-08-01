
def maybe_recover_user_shardings(
    old_shardings, new_shardings, old_avals, new_avals,
    intermediate_shardings=None, context_mesh: Mesh | None = None):
  if all(not isinstance(o, sharding_impls.GSPMDSharding) for o in new_shardings):
    return new_shardings

  for oi, o_aval in safe_zip(old_shardings, old_avals):
    if oi is not None and type(oi) in _orig_out_sharding_handlers:
      return _get_out_sharding_from_orig_sharding(
          new_shardings, new_avals, oi, o_aval)

  if intermediate_shardings is not None:
    for i in intermediate_shardings:
      if i is not None and type(i) in _orig_out_sharding_handlers:
        return _get_out_sharding_from_orig_sharding(
            new_shardings, [None] * len(new_shardings), i, None)

  # For nullary cases like: `jit(lambda: ..., out_shardings=(None, sharding))`
  for ns in new_shardings:
    if ns is not None and type(ns) in _orig_out_sharding_handlers:
      return _get_out_sharding_from_orig_sharding(
          new_shardings, new_avals, ns, None)

  if context_mesh is not None and not context_mesh.empty:
    return [sharding_impls._gspmd_to_named_sharding_via_mesh(n, context_mesh)
            if isinstance(n, GSPMDSharding) else n
            for n in new_shardings]

  return new_shardings

