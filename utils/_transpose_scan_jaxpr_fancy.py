
def _transpose_scan_jaxpr_fancy(
    jaxpr, trans_tree, trans_avals, lin_refs, immut_xs_avals) -> core.ClosedJaxpr:
  def transposed(*args):
    args = [ad.RefAccum(typeof(x).inner_aval, x) if l else x
            for l, x in zip(lin_refs, args)]
    ires, mut_consts_bar, ct_immut_consts, ct_carry, mut_xs_bar, ct_ys, eres = \
        tree_unflatten(trans_tree, args)
    immut_consts_dot = [ad.ValAccum(core.typeof(x), x) for x in ct_immut_consts]
    carry_dot = [ad.ValAccum(core.typeof(x)) for x in ct_carry]
    immut_xs_dot = [ad.ValAccum(a) for a in immut_xs_avals]
    primals = (ires + mut_consts_bar + immut_consts_dot + carry_dot + mut_xs_bar
               + immut_xs_dot + eres)
    ad.backward_pass3(jaxpr.jaxpr, False, jaxpr.consts, primals, ct_carry + ct_ys)
    return [ad.instantiate_zeros(x.freeze()) for x in primals
            if isinstance(x, ad.ValAccum)]

  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  return _make_closed_jaxpr(transposed, trans_avals, dbg)

