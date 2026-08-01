
def _remat_to_lojax(*hi_args, jaxpr, **kwds):
  closed_lo_jaxpr = pe.lower_jaxpr2(pe.close_jaxpr(jaxpr))
  lo_args = [lo_val for aval, x in zip(jaxpr.in_aval_qdds, hi_args)
             for lo_val in (aval.read_loval(x) if aval.has_qdd
                            else aval.lower_val(x))]
  lo_jaxpr = pe.convert_constvars_jaxpr(closed_lo_jaxpr.jaxpr)
  lo_args = (*closed_lo_jaxpr.consts, *lo_args)
  return remat_p.bind(*lo_args, jaxpr=lo_jaxpr, **kwds)

