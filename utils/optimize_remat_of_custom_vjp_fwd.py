
def optimize_remat_of_custom_vjp_fwd(
    fun: Callable[..., ReturnValue],
    debug_fun: core.DebugInfo,
    fwd: Callable[..., tuple[ReturnValue, Any]],
    debug_fwd: core.DebugInfo,
    nondiff_argnums: Sequence[int] = (),
    symbolic_zeros: bool = False,
) -> Callable[..., tuple[ReturnValue, Any]]:
  if symbolic_zeros:
    # TODO(dfm): This probably shouldn't be too hard to support.
    raise NotImplementedError(
        "remat optimization for custom_vjp does not support symbolic zeros")

  @wraps(fwd)
  def wrapped_fwd(*args, **kwargs) -> tuple[ReturnValue, Any]:
    # TODO(dfm): This initial logic is duplicated from custom_vjp.__call__
    # above and it would be good to consolidate it.
    # Note: we use `fun` instead of `fwd` here for consistency with
    # custom_vjp.__call__ above.
    args = resolve_kwargs(fun, args, kwargs)
    if nondiff_argnums:
      for i in nondiff_argnums: _check_for_tracers(args[i])
      nondiff_argnums_ = set(nondiff_argnums)
      dyn_argnums = [i for i in range(len(args)) if i not in nondiff_argnums_]
      f_, dyn_args = argnums_partial(lu.wrap_init(fun, debug_info=debug_fun),
                                     dyn_argnums,
                                     args, require_static_args_hashable=False)
      fwd_, _ = argnums_partial(lu.wrap_init(fwd, debug_info=debug_fwd),
                                dyn_argnums, args,
                                require_static_args_hashable=False)
    else:
      f_, dyn_args = lu.wrap_init(fun, debug_info=debug_fun), args
      fwd_ = lu.wrap_init(fwd, debug_info=debug_fwd)
    args_flat, in_tree = tree_flatten(dyn_args)
    flat_fun, out_type = _flatten_fun_nokwargs(f_, in_tree)
    flat_fwd, out_trees = _flatten_fwd(fwd_, nondiff_argnums, False,
                                       debug_fun, debug_fwd, in_tree, out_type)
    flat_fwd = _fix_fwd_args(flat_fwd)

    in_avals = [core.typeof(x) for x in args_flat]
    fwd_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fwd.with_unknown_names(),
                                                     in_avals)
    fwd_jaxpr = pe.close_jaxpr(pe.convert_constvars_jaxpr(fwd_jaxpr))
    prim_tree, res_tree, fwds = out_trees()
    num_res_out = res_tree.num_leaves - sum(f is not None for f in fwds)

    disallowed_effects = effects.custom_derivatives_allowed_effects.filter_not_in(fwd_jaxpr.effects)
    if disallowed_effects:
      raise NotImplementedError(
          "remat optimization for custom_vjp does not support forward "
          f"functions with these side effects: {disallowed_effects}")

    @pe._memoize
    def fun_jaxpr_thunk():
      jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fun, in_avals)
      return jaxpr, consts

    out_flat = remat_opt_p.bind(*consts, *args_flat, num_consts=len(consts),
                                num_res=num_res_out, fwd_jaxpr=fwd_jaxpr,
                                fun_jaxpr_thunk=fun_jaxpr_thunk)
    res, out_flat = split_list(out_flat, [num_res_out])
    res_ = iter(res)
    res = [next(res_) if f is None else args_flat[f] for f in fwds]
    assert next(res_, None) is None
    out_tree = treedef_tuple((prim_tree, res_tree))
    return tree_unflatten(out_tree, (*out_flat, *res))

  return wrapped_fwd

