
def _cond_batching_rule(axis_data, args, dims, *, branches, **params):
  index, *ops = args
  index_dim, *op_dims = dims
  # TODO(sharadmv): clean this up by adding a specific blocklist
  if any(isinstance(eff, RefEffect) for branch in branches for eff in
      branch.jaxpr.effects):
    raise NotImplementedError(
        "State effect not supported in vmap-of-cond.")
  from jax._src.callback import _IOEffect, _OrderedIOEffect
  if any(eff in branch.effects for eff in [_IOEffect, _OrderedIOEffect]
      for branch in branches):
    raise NotImplementedError(
        "IO effect not supported in vmap-of-cond.")

  if "branches_platforms" in params and (index_dim is not None):
    # If we end up with a mapped index for a platform_dependent cond, we can
    # replace the index with a fresh call to platform_index. See #29329.
    index = platform_index_p.bind(platforms=params["branches_platforms"])
    index_dim = None

  if index_dim is not None:
    # Convert to a lax.select. While we could get away with not broadcasting
    # some operands yet, because all outputs must be broadcast together anyway
    # for the select we broadcast the input operands for simplicity and leave
    # optimizations to XLA.
    # TODO(mattjj,frostig): assumes branches are side-effect-free, revise!
    index, *ops = (
        batching.bdim_at_front(x, d, axis_data.size,
                               mesh_axis=axis_data.explicit_mesh_axis)
        for x, d in zip(args, dims)
    )

    in_batched  = [True] * len(branches[0].in_avals)
    out_batched = [True] * len(branches[0].out_avals)

    branches_batched = [
        batching.batch_jaxpr(jaxpr, axis_data, in_batched, out_batched)[0]
        for jaxpr in branches]

    branch_outs = []
    for i, jaxpr in enumerate(branches_batched):
      # Perform a select on the inputs for safety of reverse-mode autodiff; see
      # https://github.com/jax-ml/jax/issues/1052
      predicate = lax.eq(index, lax._const(index, i))
      ops_ = [_bcast_select(predicate, x, lax.stop_gradient(x)) for x in ops]
      branch_outs.append(core.jaxpr_as_fun(jaxpr)(*ops_))
    out = [_bcast_select_n(index, *outs) for outs in zip(*branch_outs)]
    return out, [0 if b else None for b in out_batched]
  else:
    ops_bat = [d is not None for d in op_dims]
    ops = [batching.moveaxis(x, d, 0) if b else x
           for b, x, d in zip(ops_bat, ops, op_dims)]

    branches_out_bat = [
        batching.batch_jaxpr(jaxpr, axis_data, ops_bat, False)[1]
        for jaxpr in branches]
    out_bat = [any(bat) for bat in zip(*branches_out_bat)]
    branches_batched = tuple(
        batching.batch_jaxpr(jaxpr, axis_data, ops_bat, out_bat)[0]
        for jaxpr in branches)

    out_dims = [0 if b else None for b in out_bat]
    out = cond_p.bind(index, *ops, branches=branches_batched,
                      **params)
    return out, out_dims

