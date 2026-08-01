
def _while_loop_batching_rule(axis_data, args, dims, cond_nconsts, cond_jaxpr,
                              body_nconsts, body_jaxpr):
  from jax._src.callback import _IOEffect, _OrderedIOEffect
  if any(_OrderedIOEffect in fn.effects for fn in [body_jaxpr, cond_jaxpr]):
    raise Exception("Ordered IO effects not supported in vmap.")

  orig_batched = [d is not None for d in dims]
  cconst_bat, bconst_bat, init_bat = split_list(orig_batched, [cond_nconsts, body_nconsts])
  cconsts, bconsts, init = split_list(args, [cond_nconsts, body_nconsts])
  cconst_dims, bconst_dims, init_dims = split_list(dims, [cond_nconsts, body_nconsts])

  carry_bat = init_bat
  # Fixpoint computation of which carry are batched: either
  # batched from init, or the carry out is batched. Each iteration promotes
  # at least one carry to batched. We need at most len(carry) iterations to
  # reach a fixpoint.
  for _ in range(1 + len(carry_bat)):
    _, carry_bat_out = batching.batch_jaxpr(
        body_jaxpr, axis_data, bconst_bat + carry_bat, instantiate=carry_bat)
    if carry_bat == carry_bat_out:
      break
    carry_bat = safe_map(operator.or_, carry_bat, carry_bat_out)
  else:
    assert False, "Fixpoint not reached"

  # Knowing how the carry is batched now, we can determine if the predicate is
  # batched.
  _, (pred_bat,) = batching.batch_jaxpr(
      cond_jaxpr, axis_data, cconst_bat + carry_bat, instantiate=False)

  if pred_bat:
    # If the predicate is batched, we have to batch *all* of the carry
    # regardless of if the body needs it.
    if any(_IOEffect in fn.effects for fn in [body_jaxpr, cond_jaxpr]):
      raise Exception("Unordered IO effects not supported in while_loop "
                      "with batched predicate")
    carry_bat = [True] * len(carry_bat)
    carry_dims = [0] * len(carry_bat)
    body_jaxpr_batched, _ = batching.batch_jaxpr_axes(
        body_jaxpr, axis_data, bconst_dims + carry_dims, carry_dims)
    cond_jaxpr_batched, _ = batching.batch_jaxpr_axes(
        cond_jaxpr, axis_data, cconst_dims + carry_dims, [0])
  else:
    # If the predicate is not batched, we can look at the `cond_jaxpr`'s out
    # shape to determine the rank of the predicate. From this rank we pick the
    # dims of the carry to be batched to ensure that the predicate shape is a
    # prefix of the carry in and out shapes. We can then batch the `body_jaxpr`
    # according to these new batch dims.
    cond_rank = len(cond_jaxpr.out_avals[0].shape)
    carry_dims = [cond_rank if b else None for b in carry_bat]
    body_jaxpr_batched, _ = batching.batch_jaxpr_axes(
        body_jaxpr, axis_data, bconst_dims + carry_dims, carry_dims)
    # Now we need to rebatch the `cond_jaxpr` according to the new dims of the
    # carry.
    cond_jaxpr_batched, _ = batching.batch_jaxpr_axes(
        cond_jaxpr, axis_data, cconst_dims + carry_dims, (None,))

  # To prepare the `init` to the `while_p`, we broadcast values if they are
  # unbatched and need to have an out axis. If their current batch axis does not
  # match the one it needs to be for the translation rule to work, we move it
  # into place.
  new_init = []
  for x, old_axis, new_axis in zip(init, init_dims, carry_dims):
    if old_axis is None and new_axis is not None:
      new_init.append(batching.broadcast(x, axis_data.size, new_axis,
                                         axis_data.explicit_mesh_axis))
    elif old_axis is None and new_axis is None:
      new_init.append(x)
    else:
      assert new_axis is not None
      new_init.append(batching.moveaxis(x, old_axis, new_axis))

  outs = while_p.bind(*(cconsts + bconsts + new_init),
                      cond_nconsts=cond_nconsts, cond_jaxpr=cond_jaxpr_batched,
                      body_nconsts=body_nconsts, body_jaxpr=body_jaxpr_batched)
  return outs, carry_dims

