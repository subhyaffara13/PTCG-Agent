
def call_transpose_fancy(primitive, cts, *args, call_jaxpr, **params):
  if call_jaxpr.constvars: raise NotImplementedError
  primals_ctrefs, specs = project_accums(args)
  flat_args, treedef = tree_flatten((primals_ctrefs, cts))
  cell = lambda: None

  @partial(lu.wrap_init, debug_info=call_jaxpr.debug_info.with_unknown_names())
  def transposed(*flat_args):
    primals_ctrefs, cts = tree_unflatten(treedef, flat_args)
    args = unproject_accums(specs, primals_ctrefs)
    backward_pass3(call_jaxpr, False, (), args, cts)
    cts_out = [x.freeze() if isinstance(x, ValAccum) else None for x in args]
    cts_out, cell.out_tree = tree_flatten(cts_out)  # pyrefly: ignore[missing-attribute]
    return cts_out

  update_params = call_transpose_param_updaters.get(primitive)
  if update_params:
    params = update_params(params, [isinstance(x, GradAccum) for x in args],
                           [type(x) is not Zero for x in cts])

  out_flat = primitive.bind(*flat_args, subfuns=(transposed,), **params)
  for x, ct in zip(args, tree_unflatten(cell.out_tree, out_flat)):  # pyrefly: ignore[missing-attribute]
    if isinstance(x, ValAccum): x.accum(ct)

