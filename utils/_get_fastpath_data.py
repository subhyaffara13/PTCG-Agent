
def _get_fastpath_data(
    executable, out_tree, args_flat, out_flat, effects, consts_for_constvars,
    pgle_profiler, const_args: Sequence[ArrayLike]
    ) -> pxla.MeshExecutableFastpathData | None:
  if (
      executable is None
      or not isinstance(executable, pxla.MeshExecutable)
      or not isinstance(executable.unsafe_call, pxla.ExecuteReplicated)
      # No effects in computation
      or executable.unsafe_call.ordered_effects
      or executable.unsafe_call.has_unordered_effects
      # no ref state effects
      or any(isinstance(e, RefEffect) for e in effects)
      or _need_to_rebuild_with_fdo(pgle_profiler)
      or config.no_execution.value
  ):
    return None

  out_reflattened, out_tree = pxla.reflatten_outputs_for_dispatch(out_tree, out_flat)
  if not all(isinstance(x, xc.ArrayImpl) for x in out_reflattened):
    return None

  out_avals = [o.aval for o in out_reflattened]
  out_committed = [o._committed for o in out_reflattened]
  kept_var_bitvec = [i in executable._kept_var_idx
                      for i in range(len(const_args) + len(args_flat))]
  in_shardings = [
      sharding_impls.physical_sharding(a, s)
      if a is not core.abstract_token and dtypes.issubdtype(a.dtype, dtypes.extended)
      else s
      for s, a in zip(executable._in_shardings, executable.in_avals)
  ]
  return pxla.MeshExecutableFastpathData(
      executable.xla_executable, out_tree, in_shardings,
      executable._out_shardings, out_avals, out_committed, kept_var_bitvec,
      executable._dispatch_in_layouts, const_args)

