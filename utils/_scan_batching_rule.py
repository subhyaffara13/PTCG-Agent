
def _scan_batching_rule(axis_data, args, dims, reverse, length, jaxpr,
                        num_consts, num_carry, unroll):
  num_ys = len(jaxpr.out_avals) - num_carry
  orig_batched = [d is not None for d in dims]
  const_batched, init_batched, xs_batched = split_list(orig_batched, [num_consts, num_carry])

  # Fixpoint computation of which carry are batched: either
  # batched from init, or the carry out is batched. Each iteration promotes
  # at least one carry to batched. We need at most len(carry) iterations,
  # but we need one last iteration to prepare the jaxpr based on the final
  # carry_batched.
  carry_batched = init_batched
  for _ in range(1 + len(carry_batched)):
    batched = const_batched + carry_batched + xs_batched
    jaxpr_batched, batched_out = batching.batch_jaxpr(
        jaxpr, axis_data, batched,
        instantiate=carry_batched + [False] * num_ys)
    carry_batched_out, ys_batched = batched_out[:num_carry], batched_out[num_carry:]
    if carry_batched_out == carry_batched:
      break
    else:
      carry_batched = _map(operator.or_, carry_batched, carry_batched_out)
  else:
    assert False, "Fixpoint not reached"

  consts, init, xs = split_list(args, [num_consts, num_carry])
  consts_bdims, init_bdims, xs_bdims = split_list(dims, [num_consts, num_carry])
  new_consts = [batching.moveaxis(x, d, 0) if d is not None and d != 0
                else x for x, d in zip(consts, consts_bdims)]
  new_init = [batching.broadcast(x, axis_data.size, 0, axis_data.explicit_mesh_axis)
              if now_batched and not was_batched
              else batching.moveaxis(x, d, 0) if now_batched else x
              for x, d, was_batched, now_batched in
              zip(init, init_bdims, init_batched, carry_batched)]
  new_xs = [batching.moveaxis(x, d, 1) if d is not None and d != 1
            else x for x, d in zip(xs, xs_bdims)]
  new_args = new_consts + new_init + new_xs

  outs = scan_p.bind(
      *new_args, reverse=reverse, length=length, jaxpr=jaxpr_batched,
      num_consts=num_consts, num_carry=num_carry, unroll=unroll)
  carry_bdims = [0 if b else None for b in carry_batched]
  ys_bdims = [1 if b else None for b in ys_batched]
  return outs, carry_bdims + ys_bdims

