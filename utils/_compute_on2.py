
def _compute_on2(f, *, compute_type, out_memory_spaces, compiler_options):
  if not isinstance(compute_type, str):
    raise TypeError("`compute_on`'s compute_type argument must be a string.")
  _check_valid(compute_type)

  def wrapped(*args):
    dbg = debug_info('compute_on', f, args, {})
    args_flat, in_tree = tree_flatten(args)
    in_avals = tuple(core.shaped_abstractify(x) for x in args_flat)
    with extend_compute_type(compute_type):
      jaxpr, out_tree = _trace_to_jaxpr(f, in_avals, in_tree, dbg)
      if any(isinstance(c, core.Tracer) for c in jaxpr.consts):
        jaxpr, consts = pe.separate_consts(jaxpr)
      else:
        consts = []
    out_memory_spaces_flat = flatten_axes(
        "compute_on out_memory_spaces", out_tree, out_memory_spaces)
    compiler_options_json = (None if compiler_options is None else
                             json.dumps(compiler_options))
    outs_flat = compute_on_p.bind(
        *consts, *args_flat, jaxpr=jaxpr, compute_type=compute_type,
        out_memory_spaces=tuple(out_memory_spaces_flat),
        compiler_options_json=compiler_options_json)
    return tree_unflatten(out_tree, outs_flat)
  return wrapped

