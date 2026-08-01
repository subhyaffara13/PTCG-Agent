
def _pe_custom_params(unks_in, inst_in, kept_outs_known, kept_outs_staged,
                      in_fwd, out_fwd, out_res_specs_known, staged_in_res_specs,
                      params_known, params_staged):
  # prune inputs to jaxpr_known according to unks_in
  in_specs_known, _ = partition_list(unks_in, params_known['in_specs'])
  _, out_specs_known = partition_list(kept_outs_known, params_known['out_specs'])
  out_specs_known = out_specs_known + out_res_specs_known
  assert len(out_specs_known) == len(params_known['jaxpr'].outvars)
  new_params_known = dict(params_known, in_specs=tuple(in_specs_known),
                          out_specs=tuple(out_specs_known))

  # added num_res new inputs to jaxpr_staged, pruning according to inst_in
  _, in_specs_staged = partition_list(inst_in, params_staged['in_specs'])
  iter_staged = iter(staged_in_res_specs)
  res_specs = [in_specs_known[f1] if f1 is not None else
               out_specs_known[f2] if f2 is not None else
               next(iter_staged) for f1, f2 in zip(in_fwd, out_fwd)]

  in_specs_staged = res_specs + in_specs_staged
  _, out_specs_staged = partition_list(kept_outs_staged, params_staged['out_specs'])
  new_params_staged = dict(params_staged, in_specs=tuple(in_specs_staged),
                           out_specs=tuple(out_specs_staged))
  return new_params_known, new_params_staged

