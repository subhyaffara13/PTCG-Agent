
def _scan_linearize(is_vjp, nzs, *primals_in, reverse: bool, length: int, num_consts:
                    int, num_carry: int, jaxpr: ClosedJaxpr, unroll: int):
  const_nz, init_nz, xs_nz = split_list(nzs, [num_consts, num_carry])
  num_ys = len(jaxpr.out_avals) - num_carry
  carry_nz = init_nz
  allow_fwds = [True] * len(jaxpr.consts) + [
      (i < num_consts or i >= num_consts + num_carry)
      and not isinstance(x, np.ndarray)
      for i, x in enumerate(primals_in)
  ]
  for _ in range(1 + num_carry):
    nzs = const_nz + carry_nz + xs_nz
    primal_jaxpr, num_res_out, nzs_out, in_fwd_res, tangent_jaxpr = \
        ad.linearize_jaxpr(jaxpr, nzs, allow_fwds=allow_fwds,
                           instantiate=carry_nz + [False] * num_ys, is_vjp=is_vjp)
    carry_nz_out = nzs_out[:num_carry]
    if carry_nz_out == carry_nz:
      break
    else:
      carry_nz = _map(operator.or_, carry_nz, carry_nz_out)
  else:
    assert False, "Fixpoint not reached"
  num_res_in = len(in_fwd_res)
  num_primals_out = len(primal_jaxpr.out_avals) - num_res_out

  # At this point all non-forwarded residuals produced by primal_jaxpr are at
  # the end. We want to hoist out loop-invariant ones:
  # Before:
  #  [*const_primals_in , *carry_ext_primals_in] -> [*primals_out, *non_fwd_res]
  # After:
  #  [*const_primals_in_, *carry_ext_primals_in] -> [*primals_out, *ext_res]
  # where, modulo hoisted res not being broadcasted by the scan,
  #  non_fwd_res = merge_lists(which_hoisted, ext_res, hoisted_res)
  const_primals_in, carry_ext_primals_in = split_list(primals_in, [num_consts])
  primal_jaxpr, const_primals_in_, which_hoisted, hoisted_res = \
      _scan_known_hoisting(primal_jaxpr, const_primals_in, num_res_out)
  del num_res_out

  # To make tangent_jaxpr match the scan calling convention, move to the back
  # binders that don't correspond to hoisted or const-forwarded residuals.
  #   Before: [*res, *tangents_in] -> [*tangents_out]
  #   After: [*int_res, *tangents_in, *ext_res] -> [*tangents_out]
  num_tangents_in = len(tangent_jaxpr.in_avals) - num_res_in
  which_hoisted_ = iter(which_hoisted)
  res_to_move = [not next(which_hoisted_) if f is None else
                 f >= len(jaxpr.consts) + num_consts + num_carry
                 for f in in_fwd_res]
  assert next(which_hoisted_, None) is None
  tangent_jaxpr = pe.move_binders_to_back(
      tangent_jaxpr, res_to_move + [False] * num_tangents_in)

  # Run the primal scan (if it has any outputs or effects).
  if not primal_jaxpr.out_avals and not primal_jaxpr.effects:
    out = []
  else:
    out = scan_p.bind(*const_primals_in_, *carry_ext_primals_in,
                      jaxpr=primal_jaxpr, reverse=reverse, length=length,
                      num_consts=len(const_primals_in_), num_carry=num_carry,
                      unroll=unroll)
  primals_out, ext_res = split_list(out, [num_primals_out])

  # Complete res using hoisted_res and input forwards.
  res = subs_list(in_fwd_res, [*jaxpr.consts, *primals_in],
                  merge_lists(which_hoisted, ext_res, hoisted_res))

  def tangent_fun(res, *tangents):
    int_res, ext_res = partition_list(res_to_move, res)
    nz_tangents = [ad.instantiate_zeros(x) for nz, x in zip(nzs, tangents) if nz]
    tangent_num_consts = len(int_res) + sum(nzs[:num_consts])
    tangent_num_carry = sum(nzs[num_consts:num_consts + num_carry])
    nz_tangents_out = scan_p.bind(
        *int_res, *nz_tangents, *ext_res, jaxpr=tangent_jaxpr, reverse=reverse,
        length=length, num_consts=tangent_num_consts,
        num_carry=tangent_num_carry, unroll=unroll)
    tangent_avals_out = [v.aval.to_tangent_aval() for v in jaxpr.jaxpr.outvars]
    nz_tangents_out_ = iter(nz_tangents_out)
    tangents_out = [next(nz_tangents_out_) if nz else ad.Zero(aval)
                    for aval, nz in zip(tangent_avals_out, nzs_out)]
    assert next(nz_tangents_out_, None) is None
    return tangents_out

  return primals_out, nzs_out, res, tangent_fun

