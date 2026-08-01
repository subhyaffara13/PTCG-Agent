
def _scan_jvp(primals, tangents, reverse, length, jaxpr, num_consts, num_carry,
              unroll):
  num_xs = len(jaxpr.in_avals) - num_carry - num_consts
  num_ys = len(jaxpr.out_avals) - num_carry
  nonzeros = [type(t) is not ad_util.Zero for t in tangents]
  const_nz, init_nz, xs_nz = split_list(nonzeros, [num_consts, num_carry])

  # Fixpoint computation of which carry are not ad.zero: either
  # non-zero from init, or the carry out is non-zero. Each iteration promotes
  # at least one carry to non-zero. We need at most len(carry) iterations,
  # but we need one last iteration to prepare the jaxpr based on the final
  # carry_nz.
  carry_nz = init_nz
  for _ in range(1 + len(carry_nz)):
    nonzeros = const_nz + carry_nz + xs_nz
    jaxpr_jvp, nonzeros_out = ad.jvp_jaxpr(
        jaxpr, nonzeros, instantiate=carry_nz + [False] * num_ys)
    carry_nz_out, _ = nonzeros_out[:num_carry], nonzeros_out[num_carry:]
    if carry_nz_out == carry_nz:
      break
    else:
      carry_nz = _map(operator.or_, carry_nz, carry_nz_out)
  else:
    assert False, "Fixpoint not reached"

  tangents = [ad.instantiate_zeros(t) if nz else t
              for t, nz in zip(tangents, nonzeros)]

  consts, init, xs = split_list(primals, [num_consts, num_carry])
  all_tangents = split_list(tangents, [num_consts, num_carry])
  consts_dot, init_dot, xs_dot = _map(_prune_zeros, all_tangents)

  jaxpr_jvp_rearranged = ad.rearrange_binders(
      jaxpr_jvp,
      [num_consts, num_carry, num_xs], [len(consts_dot), len(init_dot), len(xs_dot)],
      [num_carry, num_ys], [len(init_dot), sum(nonzeros_out) - len(init_dot)])

  out_flat = scan_p.bind(
      *(consts + consts_dot + init + init_dot + xs + xs_dot),
      reverse=reverse, length=length, jaxpr=jaxpr_jvp_rearranged,
      num_consts=num_consts + len(consts_dot),
      num_carry=num_carry + len(init_dot), unroll=unroll)

  carry, carry_dot, ys, ys_dot = split_list(out_flat, [num_carry, len(init_dot), num_ys])
  primals_out = carry + ys
  tangents_out_iter = iter(carry_dot + ys_dot)
  tangents_out = [next(tangents_out_iter) if nz else ad_util.p2tz(p)
                  for p, nz in zip(primals_out, nonzeros_out)]
  return primals_out, tangents_out

