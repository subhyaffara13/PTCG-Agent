
def _maybe_get_and_check_out_shardings(
    xla_executable, out_shardings, device_list, global_out_avals,
    num_ordered_effects
  ):
  out_shardings_xla = get_out_shardings_from_executable(
      xla_executable, device_list, len(global_out_avals),
      num_ordered_effects)
  if out_shardings_xla is None:
    return out_shardings

  new_out_shardings = []
  for xla_s, orig, aval in safe_zip(out_shardings_xla, out_shardings,
                                    global_out_avals):
    if isinstance(orig, UnspecifiedValue):
      if (aval is not core.abstract_token and
          dtypes.issubdtype(aval.dtype, dtypes.extended)):
        xla_s = sharding_impls.logical_sharding(aval.shape, aval.dtype, xla_s)
      new_out_shardings.append(xla_s)
    elif mlir.contains_unconstrained(orig):
      is_subdtype = dtypes.issubdtype(aval.dtype, dtypes.extended)
      if aval is not core.abstract_token and is_subdtype:
        xla_s = sharding_impls.logical_sharding(aval.shape, aval.dtype, xla_s)
      if (not is_subdtype and not aval.sharding.mesh.empty and
          not aval.sharding.mesh._any_axis_manual and
          op_shardings.are_hlo_shardings_equal(
              aval.sharding._to_xla_hlo_sharding(aval.ndim),
              xla_s._to_xla_hlo_sharding(aval.ndim))):
        conc_mesh = _abstract_to_concrete_mesh(
            aval.sharding.mesh, xla_s._device_assignment)
        new_out_shardings.append(aval.sharding.update(mesh=conc_mesh))
      else:
        try:
          new_out_shardings.append(_gspmd_to_named_sharding(xla_s, aval, orig))  # type: ignore
        except:
          new_out_shardings.append(xla_s)
    else:
      xla_hlo_s = xla_s._to_xla_hlo_sharding(aval.ndim)
      orig_hlo_s = orig._to_xla_hlo_sharding(aval.ndim)
      # MANUAL HloSharding comes from other partitioning frameworks.
      if (not dtypes.issubdtype(aval.dtype, dtypes.extended) and
          not xla_hlo_s.is_manual() and aval.size != 0 and
          (not op_shardings.are_hlo_shardings_equal(xla_hlo_s, orig_hlo_s) or
           xla_s.memory_kind != orig.memory_kind)):
        raise AssertionError(
            f"Unexpected XLA sharding override: (XLA) {xla_s} != {orig} "
            "(User sharding)")
      new_out_shardings.append(orig)
  return new_out_shardings

