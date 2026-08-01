
def _while_loop_jvp(primals, tangents, cond_nconsts, cond_jaxpr, body_nconsts,
                    body_jaxpr):
  nonzeros = [type(t) is not ad_util.Zero for t in tangents]
  cconst_nz, bconst_nz, init_nz = split_list(nonzeros, [cond_nconsts, body_nconsts])

  carry_nz = init_nz
  for _ in range(1 + len(carry_nz)):
    body_nonzeros = bconst_nz + carry_nz
    body_jvp, nonzeros_out = ad.jvp_jaxpr(
        body_jaxpr, body_nonzeros, instantiate=carry_nz)
    if nonzeros_out == carry_nz:
      break
    carry_nz = _map(operator.or_, carry_nz, nonzeros_out)
  else:
    assert False, "Fixpoint not reached"

  nonzeros = cconst_nz + body_nonzeros
  tangents = [ad.instantiate_zeros(t) if nz else t
              for t, nz in zip(tangents, nonzeros)]

  cconst, bconst, init = split_list(primals, [cond_nconsts, body_nconsts])
  _, bconst_dot, init_dot = split_list(tangents, [cond_nconsts, body_nconsts])
  bconst_dot = _prune_zeros(bconst_dot)
  init_dot = _prune_zeros(init_dot)

  num_carry = len(primals) - cond_nconsts - body_nconsts

  body_jvp_rearranged = ad.rearrange_binders(
      body_jvp,
      [body_nconsts, num_carry], [len(bconst_dot), len(init_dot)],
      [num_carry], [len(init_dot)])

  newvar = core.gensym()
  invars_aug = cond_jaxpr.jaxpr.invars + [newvar(core.typeof(x)) for x in init_dot]
  cond_debug = cond_jaxpr.jaxpr.debug_info
  augmented_debug = cond_debug
  if cond_debug is not None and cond_debug.arg_names is not None:
    augmented_debug = cond_debug._replace(
        arg_names=cond_debug.arg_names + ('',) * len(init_dot))
  cond_jaxpr_augmented = cond_jaxpr.jaxpr.replace(
      invars=invars_aug, debug_info=augmented_debug)
  cond_jaxpr_augmented = ClosedJaxpr(cond_jaxpr_augmented, cond_jaxpr.consts)

  out = while_p.bind(
      *(cconst + bconst + bconst_dot + init + init_dot),
      cond_nconsts=cond_nconsts,
      cond_jaxpr=cond_jaxpr_augmented,
      body_nconsts=len(bconst) + len(bconst_dot),
      body_jaxpr=body_jvp_rearranged)

  out_carry, out_carry_dot = split_list(out, [num_carry])
  out_tangents_iter = iter(out_carry_dot)
  out_tangents = [next(out_tangents_iter) if nz else ad_util.p2tz(p)
                  for p, nz in zip(out_carry, nonzeros_out)]
  return out_carry, out_tangents

