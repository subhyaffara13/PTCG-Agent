
def _spec_rank_error(
    error_type: SpecErrorType, f: Callable, tree: PyTreeDef, specs: Specs,
    fails: list[core.ShapedArray | NoFail]) -> str:
  fun_name = util_fun_name(f)
  if error_type == SpecErrorType.input:
    prefix, base = 'in', 'the passed args'
    ba = _try_infer_args(f, tree)
  else:
    prefix, base = 'out', f'{fun_name}(*args)'
    ba = None
  msgs = []
  for (spec_key, spec), (fail_key, aval) in _iter_paths(tree, specs, fails):
    extra = ""
    if error_type == SpecErrorType.input and ba is not None:
      arg_key, *_ = fail_key
      param_names, params = unzip2(
          (name, param) for name, param in ba.signature.parameters.items()
          if param.kind not in (inspect.Parameter.KEYWORD_ONLY,
                                inspect.Parameter.VAR_KEYWORD))
      if (arg_key.idx >= len(params) or
          params[arg_key.idx].kind == inspect.Parameter.VAR_POSITIONAL):
        extra = (f", where args{arg_key} is the index "
                 f"{arg_key.idx - len(params) + 1} component "
                 f"of {fun_name}'s varargs parameter '{param_names[-1]}',")
      else:
        param_name = params[arg_key.idx]
        extra = (f", where args{arg_key} is bound to {fun_name}'s "
                 f"parameter '{param_name}',")
    msgs.append(
        f"* {prefix}_specs{keystr(spec_key)} is {spec} which has length "
        f"{len(spec)}, but "
        f"{base}{keystr(fail_key)}{extra} has shape {aval.str_short()}, "
        f"which has rank {aval.ndim} (and {aval.ndim} < {len(spec)})")
  assert msgs
  if len(msgs) == 1: msgs = [msgs[0][2:]]  # remove the bullet point
  msg = (f"shard_map applied to the function '{fun_name}' was given an "
         f"{prefix}_specs entry which is too long to be compatible with the "
         f"corresponding {prefix}put value from the function:\n\n"
         + '\n\n'.join(msgs) + '\n\n' +
         f"Entries in {prefix}_specs must be of length no greater than the "
         f"number of axes in the corresponding {prefix}put value.\n\n"
         f"Either revise the spec to be shorter, or modify '{fun_name}' so "
         f"that its {prefix}puts have sufficient rank.")
  if any(not aval.ndim for _, (_, aval) in _iter_paths(tree, specs, fails)):
    msg += (f"\n\nFor scalar values (rank 0), consider using an {prefix}_specs "
            "entry of `P()`, where `P = jax.sharding.PartitionSpec`.")
  return msg

