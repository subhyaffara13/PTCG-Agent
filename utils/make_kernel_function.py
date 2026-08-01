
def make_kernel_function(
    jaxpr: core.Jaxpr,
    consts,
    in_tree,
    out_tree,
    read_usage_env,
    in_block_specs,
    block_spec_env,
    scalar_prefetch_handler,
    grid_len,
):
  in_avals = [v.aval for v in jaxpr.invars]
  invar_usages = util.safe_map(read_usage_env, jaxpr.invars)
  bs_env, scalar_prefetch_fn_env = block_spec_env

  def _remove_nones(
      shape: tuple[pallas_core.BlockDim | int | None, ...] | None,
  ) -> tuple[int, ...]:
    new_shape = tuple(_block_size(s) for s in shape)
    return tuple(s for s in new_shape if s is not None)

  _no_aval = object()

  def _get_block_aval(bs, aval):
    if isinstance(aval, state.AbstractRef):
      return aval
    if bs is pallas_core.no_block_spec or bs is None:
      return _no_aval
    if bs.block_shape is None:
      return aval
    return aval.update(shape=_remove_nones(bs.block_shape))

  in_block_avals = [
      _get_block_aval(bs, aval)
      for aval, bs in zip(in_avals, in_block_specs, strict=True)
  ]
  unflat_in_block_arg_avals, unflat_in_block_kwarg_avals = (
      tree_util.tree_unflatten(in_tree, in_block_avals)
  )

  kernel_in_type = (unflat_in_block_arg_avals, unflat_in_block_kwarg_avals)

  def _read_block_spec(atom: core.Atom) -> pallas_core.BlockSpec | Any:
    if isinstance(atom, core.Literal):
      return pallas_core.no_block_spec
    return bs_env.get(atom, pallas_core.no_block_spec)

  def kernel_fn(program_ids, scalar_prefetch, *args, **kwargs):
    flat_args, in_tree_ = tree_util.tree_flatten((args, kwargs))
    if in_tree_ != tree_util.tree_structure(kernel_in_type):
      raise ValueError(f'Expected {kernel_in_type} PyTree, got {in_tree_}')
    env = {}

    def read_env(atom):
      match atom:
        case core.Literal():
          return atom.val
        case core.Var():
          return env.get(atom, None)

    def write_env(var, val):
      env[var] = val

    for const, constvar in zip(consts, jaxpr.constvars):
      env[constvar] = const
    for invar, arg, usage in zip(jaxpr.invars, flat_args, invar_usages):
      if Usage.REGULAR in usage:
        env[invar] = arg
    for i, eqn in enumerate(jaxpr.eqns):
      outvar_usages = [
          read_usage_env(v) if not isinstance(v, core.Literal) else set()
          for v in eqn.outvars
      ]
      if any(Usage.REGULAR in usage for usage in outvar_usages):
        in_vals = util.safe_map(read_env, eqn.invars)
        # TODO(sharadmv,justinfu): preserve source mapping
        if not (eval_rule := eval_rules.get(eqn.primitive, None)):
          raise NotImplementedError(eqn.primitive)
        out_block_specs = tuple(util.safe_map(_read_block_spec, eqn.outvars))
        in_block_specs = tuple(util.safe_map(_read_block_spec, eqn.invars))
        out_usages = tuple(read_usage_env(v) for v in eqn.outvars)
        # We need to substitute in scalar prefetch values into equation invars.
        if scalar_prefetch_fn := scalar_prefetch_fn_env.get(i, None):
          # Evaluate scalar prefetch function.
          with _sp_context(*scalar_prefetch):
            scalar_prefetch_vals = scalar_prefetch_fn()
          # Some results of the SP function will be literals.
          eqn_invar_usages = [
              read_usage_env(v)
              if not isinstance(v, core.Literal)
              else {Usage.SCALAR_PREFETCH}
              for v in eqn.invars
          ]
          sp_iter = iter(scalar_prefetch_vals)
          for i, usage in enumerate(eqn_invar_usages):
            if usage == {Usage.SCALAR_PREFETCH}:
              if not isinstance(eqn.invars[i], core.Literal):
                in_vals[i] = next(sp_iter)
        eval_ctx = KernelEvalContext(
            avals_in=tuple(v.aval for v in eqn.invars),
            avals_out=tuple(v.aval for v in eqn.outvars),
            scalar_prefetch=scalar_prefetch,
            program_ids=tuple(program_ids),
            in_block_specs=in_block_specs,
            out_block_specs=out_block_specs,
            scalar_prefetch_handler=scalar_prefetch_handler,
            grid_len=grid_len,
            out_usages=out_usages,
        )
        outs = eval_rule(eval_ctx, *in_vals, **eqn.params)
        if not eqn.primitive.multiple_results:
          outs = [outs]
        util.safe_map(write_env, eqn.outvars, outs)
    out = util.safe_map(read_env, jaxpr.outvars)
    return tree_util.tree_unflatten(out_tree, out)

  return kernel_fn

