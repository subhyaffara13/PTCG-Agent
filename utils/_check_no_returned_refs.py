
def _check_no_returned_refs(
    dbg: core.DebugInfo,
    out_tracers: Sequence[DynamicJaxprTracer]
) -> None:
  if not config.mutable_array_checks.value: return
  for i, t in enumerate(out_tracers):
    a = t.aval
    if isinstance(a, AbstractRef):
      result_paths = dbg.resolve_result_paths().safe_result_paths(len(out_tracers))
      if list(result_paths) == ["result"]: result_paths = [""]  # TODO(mattjj): fix in callee
      loc = result_paths[i] and f' at output tree path {result_paths[i]}'
      frame = t._trace.frame
      v = t.val
      eqns = frame.get_eqns()
      # TODO(dougalm): something more efficient
      eqn = next((e for e in eqns if v in e.outvars), None)
      if eqn:
        assert eqn.primitive is core.ref_p
        origin_info = ('\n\nThe returned mutable array was created on line '
                       f'{source_info_util.summarize(eqn.source_info)}.')
      elif v in frame.invars:
        assert isinstance(v, Var)
        arg_name = dbg.safe_arg_names(len(frame.invars))[frame.invars.index(v)]
        origin_info = ('\n\nThe returned mutable array was passed in as the '
                       f'argument {arg_name}.')
      else:
        origin_info = ''
      raise ValueError(
          f"function {dbg.func_src_info} traced for {dbg.traced_for} returned "
          f"a mutable array reference of type {a.str_short()}{loc}, but "
          f"mutable array references cannot be returned.{origin_info}")

