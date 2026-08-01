
def custom_vmap_jvp(primals, tangents, *,
                    call: core.ClosedJaxpr,
                    rule: ClosedRule,
                    in_tree: tree_util.PyTreeDef, out_tree: tree_util.PyTreeDef):
  def jvp_of_rule_rule(axis_size: int, in_batched, primals, tangents):
    in_batched_ps, in_batched_ts = in_batched

    mutually_batched = tree_map(operator.and_, in_batched_ps, in_batched_ts)
    extra_batched_ps = tree_map(lambda pb, tb: 0 if pb and not tb else None,
                                in_batched_ps, in_batched_ts)
    extra_batched_ts = tree_map(lambda pb, tb: 0 if tb and not pb else None,
                                in_batched_ps, in_batched_ts)

    out_mutually_batched = lu.Store()
    flat_ps_ts, tree_ps_ts = tree_flatten((primals, tangents))
    flat_extra_batched_ps_ts, tree_ps_ts2 = tree_flatten(
        (extra_batched_ps, extra_batched_ts),
        is_leaf=lambda x: x is None)

    # TODO(frostig): assert these also equal:
    #   treedef_tuple((in_tree, in_tree))
    # once https://github.com/jax-ml/jax/issues/9066 is fixed
    assert tree_ps_ts == tree_ps_ts2
    del tree_ps_ts2

    def to_jvp(*primals):
      out, out_batched = call_rule(rule, axis_size, mutually_batched, primals)
      check_vmap_rule_trees(
          rule, out_tree, tree_structure(out), tree_structure(out_batched))
      out_mutually_batched.store(out_batched)
      return out

    api_util.save_wrapped_fun_debug_info(to_jvp, call.jaxpr.debug_info)
    def to_vmap_over_extra_batched_dims(primals, tangents):
      return api.jvp(to_jvp, primals, tangents)

    to_vmap_over_extra_batched_dims_flat, out_tree2 = api_util.flatten_fun_nokwargs(
        lu.wrap_init(to_vmap_over_extra_batched_dims,
                     # TODO(necula): fix the debug_info calling convention
                     debug_info=call.jaxpr.debug_info),
        tree_ps_ts)

    flat_out_ps_ts, flat_out_axes = vmap_unrestricted(
        to_vmap_over_extra_batched_dims_flat, *flat_ps_ts,
        in_axes=flat_extra_batched_ps_ts,
        axis_name=core.no_axis_name, axis_size=axis_size)

    n, ragged = divmod(len(flat_out_ps_ts), 2)
    assert not ragged
    flat_out_ps, flat_out_ts = flat_out_ps_ts[:n], flat_out_ps_ts[n:]
    flat_out_axes_p, flat_out_axes_t = flat_out_axes[:n], flat_out_axes[n:]
    flat_out_ps = map(maybe_bdim_at_front, flat_out_ps, flat_out_axes_p)
    flat_out_extra_batched_ps = [d is not None for d in flat_out_axes_p]
    flat_out_ts = map(maybe_bdim_at_front, flat_out_ts, flat_out_axes_t)
    flat_out_extra_batched_ts = [d is not None for d in flat_out_axes_t]

    out_ps, out_ts = tree_unflatten(
        out_tree2(), [*flat_out_ps, *flat_out_ts])
    out_extra_batched_ps, out_extra_batched_ts = tree_unflatten(
        out_tree2(), [*flat_out_extra_batched_ps, *flat_out_extra_batched_ts])

    out_batched_ps = tree_map(
        operator.or_, out_mutually_batched.val, out_extra_batched_ps)
    out_batched_ts = tree_map(
        operator.or_, out_mutually_batched.val, out_extra_batched_ts)

    return (out_ps, out_ts), (out_batched_ps, out_batched_ts)

  tangents = map(ad.instantiate_zeros, tangents)
  jvp_call, _ = ad.jvp_jaxpr(call, [True] * len(primals), True)
  jvp_in_tree = treedef_tuple((in_tree, in_tree))
  jvp_out_tree = treedef_tuple((out_tree, out_tree))
  outs = custom_vmap_p.bind(
      *primals, *tangents,
      call=jvp_call, rule=jvp_of_rule_rule,
      in_tree=jvp_in_tree, out_tree=jvp_out_tree)
  assert len(outs) % 2 == 0, len(outs)
  out_primals, out_tangents = util.split_list(outs, [len(outs) // 2])
  return out_primals, out_tangents

