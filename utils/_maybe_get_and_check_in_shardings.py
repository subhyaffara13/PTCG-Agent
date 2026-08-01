
def _maybe_get_and_check_in_shardings(
    xla_executable, in_shardings, device_list, global_in_avals,
    num_ordered_effects):
  """Returns in_shardings extracted from XLA or checks and returns original
  shardings.

  If in_shardings exist on `jit` or on `jax.Array`, then this function will
  check that sharding against what XLA returns as in_shardings. If they don't
  match, an error is raised.

  If in_sharding is unspecified, then the sharding returned by XLA is returned.
  """
  in_shardings_xla = _get_in_shardings_from_xla(
      xla_executable, device_list, len(global_in_avals), num_ordered_effects)
  if in_shardings_xla is None:
    return in_shardings

  new_in_shardings = []
  for xla_s, orig, aval in safe_zip(in_shardings_xla, in_shardings,
                                    global_in_avals):
    if isinstance(orig, UnspecifiedValue):
      if (aval is not core.abstract_token and
          dtypes.issubdtype(aval.dtype, dtypes.extended)):
        xla_s = sharding_impls.logical_sharding(aval.shape, aval.dtype, xla_s)
      new_in_shardings.append(xla_s)
    else:
      xla_hlo_s = xla_s._to_xla_hlo_sharding(aval.ndim)
      orig_hlo_s = orig._to_xla_hlo_sharding(aval.ndim)
      # MANUAL HloSharding comes from other partitioning frameworks.
      if (not dtypes.issubdtype(aval.dtype, dtypes.extended) and
          not xla_hlo_s.is_manual() and
          (not op_shardings.are_hlo_shardings_equal(xla_hlo_s, orig_hlo_s))):
        raise AssertionError(
            f"Unexpected XLA sharding override: (XLA) {xla_s} != {orig} "
            "(User sharding)")
      new_in_shardings.append(orig)

  new_in_shardings = maybe_recover_user_shardings(
      in_shardings, new_in_shardings, global_in_avals, global_in_avals)

  return new_in_shardings

