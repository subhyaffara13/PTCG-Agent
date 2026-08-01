
def _lojax_expand_params(
    in_avals_, out_avals, donated_invars, in_shardings, in_layouts,
    out_shardings, out_layouts, **params):
  in_avals, () = in_avals_.unpack()
  in_lol = in_avals.unpack()
  mut_out_lol, out_lol_ = out_avals.unpack()
  out_lol = out_lol_.unpack()

  # some pjit params match the length of hi_jaxpr.invars/outvars, so when
  # lowering we must expand them to match their number of lojax types
  def expand(lol, stuff):
    return tuple(x for l, x in zip(lol, stuff) for _ in l)
  donated_invars = expand(in_lol , donated_invars)
  in_shardings   = expand(in_lol , in_shardings  )
  in_layouts     = expand(in_lol , in_layouts    )
  out_shardings  = expand(out_lol, out_shardings )
  out_layouts    = expand(out_lol, out_layouts   )

  # also, the lo_jaxpr has pure outputs corresponding to mutable hi_jaxpr types
  num_muts_out = len(mut_out_lol)  # it's a flat tree
  out_shardings = (UNSPECIFIED,) * num_muts_out + out_shardings
  out_layouts = (None,) * num_muts_out + out_layouts

  new_params = dict(params, donated_invars=donated_invars,
                    in_shardings=in_shardings, in_layouts=in_layouts,
                    out_shardings=out_shardings, out_layouts=out_layouts)
  return new_params

