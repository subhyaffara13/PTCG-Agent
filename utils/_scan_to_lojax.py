
def _scan_to_lojax(*hi_args, jaxpr, num_carry, num_consts, **params):
  # move qdd binders and corresponding hi_args from consts slots to carry slots
  to_move = [t.has_qdd and not t.is_writer for t in jaxpr.in_aval_qdds[:num_consts]]
  jaxpr = pe.move_invars_right(jaxpr, to_move)
  hi_args = _move_right(hi_args, to_move)
  num_consts -= sum(to_move)
  num_carry += sum(to_move)

  const, carry, ext = split_list(hi_args, [num_consts, num_carry])
  const_qdds, carry_qdds, ext_qdds = split_list(jaxpr.in_aval_qdds, [num_consts, num_carry])
  const_lol = [a.read_loval_in(x) if a.has_qdd else a.lower_val(x)
               for a, x in zip(const_qdds, const)]
  carry_lol = [a.read_loval_in(x) if a.has_qdd else a.lower_val(x)
               for a, x in zip(carry_qdds, carry)]
  ext_lol   = [a.read_loval_in(x) if a.has_qdd else a.lower_val(x)
               for a, x in zip(ext_qdds, ext)]
  num_lo_consts = sum(len(xs) for xs in const_lol)
  num_lo_carry  = sum(len(xs) for xs in carry_lol)
  lo_args_lol = [*const_lol, *carry_lol, *ext_lol]
  rrtype = lambda x: core.mapped_leading_aval(params['length'], typeof(x))
  in_avals_lol = [*[[typeof(x) for x in xs] for xs in const_lol],
                  *[[typeof(x) for x in xs] for xs in carry_lol],
                  *[[rrtype(x) for x in xs] for xs in ext_lol]]
  in_avals = FlatTree.flatten((in_avals_lol, {}))

  lo_jaxpr, out_avals = pe.lower_jaxpr(jaxpr, in_avals)

  # move extensive outputs
  out_mut_avals, _ = out_avals.unpack()
  const_mut, carry_mut, ext_mut = split_list(out_mut_avals.unpack(), [num_consts, num_carry])
  num_const_mut = sum(len(xs) for xs in const_mut)
  num_carry_mut = sum(len(xs) for xs in carry_mut)
  num_ext_mut   = sum(len(xs) for xs in ext_mut)
  num_rest = len(lo_jaxpr.out_avals) - num_const_mut - num_carry_mut - num_ext_mut
  to_move = ([True] * num_const_mut + [False] * num_carry_mut +
             [True] * num_ext_mut + [False] * num_rest)
  lo_jaxpr = pe.move_outvars_to_back(lo_jaxpr, to_move)

  lo_args = [x for xs in lo_args_lol for x in xs]
  all_outs = scan_p.bind(*lo_args, jaxpr=lo_jaxpr, num_consts=num_lo_consts,
                         num_carry=num_lo_carry, **params)
  carry_mut, rest, const_mut, ext_mut = split_list_checked(
      all_outs, [num_carry_mut, num_rest, num_const_mut, num_ext_mut])
  all_outs = [*const_mut, *carry_mut, *ext_mut, *rest]

  out_mut, lo_outs = out_avals.update(all_outs).unpack()
  for a, x, u in zip(jaxpr.final_aval_qdds, hi_args, out_mut.unpack()):
    if a.has_qdd:
      a.aval.update_from_loval2(a.qdd, x, u)
  return [a.raise_val2(y) for a, y in zip(jaxpr.out_avals, lo_outs.unpack())]

