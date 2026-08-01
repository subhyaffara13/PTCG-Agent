
def _while_to_lojax(*hi_args, cond_jaxpr, body_jaxpr, cond_nconsts, body_nconsts):
  if any(a.has_qdd for a in cond_jaxpr.in_avals[:cond_nconsts]):
    raise NotImplementedError  # TODO(mattjj,dougalm)
  assert not any(a.has_qdd for a in cond_jaxpr.in_avals[cond_nconsts:])

  hi_cconsts, hi_bconsts, hi_carry = split_list(hi_args, [cond_nconsts, body_nconsts])

  # move qdd binders and corresponding hi_args from consts slots to carry slots
  to_move = [t.has_qdd for t in body_jaxpr.in_aval_qdds[:body_nconsts]]
  body_jaxpr = pe.move_invars_right(body_jaxpr, to_move)
  hi_bconsts, hi_bconsts_qdd = partition_list(to_move, hi_bconsts)
  hi_carry = [*hi_bconsts_qdd, *hi_carry]
  body_nconsts -= sum(to_move)
  cond_jaxpr = _insert_binders(cond_jaxpr, cond_nconsts, hi_bconsts_qdd)
  del hi_bconsts_qdd

  # collect input values
  loval = lambda a, x: a.read_loval(x) if a.has_qdd else a.lower_val(x)
  lovals = lambda avals, xs: [lo for a, x in zip(avals, xs) for lo in loval(a, x)]
  lo_cconsts = lovals(cond_jaxpr.in_aval_qdds[:cond_nconsts], hi_cconsts)
  lo_bconsts = lovals(body_jaxpr.in_aval_qdds[:body_nconsts], hi_bconsts)
  lo_carry = lovals(body_jaxpr.in_aval_qdds[body_nconsts:], hi_carry)

  # expand cond_nconsts and body_nconsts according to lo types
  cond_nconsts = sum(len(typeof(x).lo_ty()) for x in hi_cconsts)
  body_nconsts = sum(len(typeof(x).lo_ty()) for x in hi_bconsts)

  # lower jaxprs and bind
  in_avals = FlatTree.flatten(([a.lo_ty() for a in body_jaxpr.in_aval_qdds], {}))
  lo_body_jaxpr, out_avals = pe.lower_jaxpr(body_jaxpr, in_avals)
  all_outs = while_p.bind(*lo_cconsts, *lo_bconsts, *lo_carry,
                          cond_jaxpr=pe.lower_jaxpr2(cond_jaxpr),
                          body_jaxpr=lo_body_jaxpr,
                          cond_nconsts=cond_nconsts, body_nconsts=body_nconsts)
  out_mut, lo_outs = out_avals.update(all_outs).unpack()
  for a, x, u in zip(body_jaxpr.final_aval_qdds, it.chain(hi_bconsts, hi_carry), out_mut.unpack()):
    if a.has_qdd:
      a.aval.update_from_loval2(a.qdd, x, u)
  return [a.raise_val2(y) for a, y in zip(body_jaxpr.out_avals, lo_outs.unpack())]

