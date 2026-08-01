
def _add_res_to_params(num_res, in_shardings, out_shardings, in_layouts,
                       out_layouts, donated_invars, **params):
  params_fwd = dict(params,
                    in_shardings=in_shardings,
                    out_shardings=out_shardings + (UNSPECIFIED,) * num_res,
                    in_layouts=in_layouts,
                    out_layouts=out_layouts + (None,) * num_res,
                    donated_invars=donated_invars)
  params_rem = dict(params,
                    in_shardings=(UNSPECIFIED,) * num_res + in_shardings,
                    out_shardings=out_shardings,
                    in_layouts=(None,) * num_res + in_layouts,
                    out_layouts=out_layouts,
                    donated_invars=(False,) * num_res + donated_invars)
  return params_fwd, params_rem

