
def _pjit_partial_eval_custom_params_updater(
    unks_in: Sequence[bool], inst_in: Sequence[bool],
    kept_outs_known: Sequence[bool], kept_outs_staged: Sequence[bool],
    num_res_out: int, num_res_in: int, params_known: dict, params_staged: dict
  ) -> tuple[dict, dict]:
  # prune inputs to jaxpr_known according to unks_in
  donated_invars_known, _ = pe.partition_list(unks_in, params_known['donated_invars'])
  in_shardings_known, _ = pe.partition_list(unks_in, params_known['in_shardings'])
  _, out_shardings_known = pe.partition_list(kept_outs_known, params_known['out_shardings'])
  in_layouts_known, _ = pe.partition_list(unks_in, params_known['in_layouts'])
  _, out_layouts_known = pe.partition_list(kept_outs_known, params_known['out_layouts'])

  new_params_known = dict(params_known,
                          in_shardings=tuple(in_shardings_known),
                          out_shardings=(*out_shardings_known,
                                         *[UNSPECIFIED] * num_res_out),
                          in_layouts=tuple(in_layouts_known),
                          out_layouts=(*out_layouts_known, *[None] * num_res_out),
                          donated_invars=tuple(donated_invars_known))
  assert len(new_params_known['in_shardings']) == len(params_known['jaxpr'].in_avals)
  assert len(new_params_known['out_shardings']) == len(params_known['jaxpr'].out_avals)
  assert len(new_params_known['in_layouts']) == len(params_known['jaxpr'].in_avals)
  assert len(new_params_known['out_layouts']) == len(params_known['jaxpr'].out_avals)

  # added num_res new inputs to jaxpr_staged, and pruning according to inst_in
  _, donated_invars_staged = pe.partition_list(inst_in, params_staged['donated_invars'])
  donated_invars_staged = [False] * num_res_in + donated_invars_staged
  _, in_shardings_staged = pe.partition_list(inst_in, params_staged['in_shardings'])
  in_shardings_staged = [*[UNSPECIFIED] * num_res_in, *in_shardings_staged]
  _, out_shardings_staged = pe.partition_list(kept_outs_staged, params_staged['out_shardings'])
  _, in_layouts_staged = pe.partition_list(inst_in, params_staged['in_layouts'])
  in_layouts_staged = [*[None] * num_res_in, *in_layouts_staged]
  _, out_layouts_staged = pe.partition_list(kept_outs_staged, params_staged['out_layouts'])

  new_params_staged = dict(params_staged,
                           in_shardings=tuple(in_shardings_staged),
                           out_shardings=tuple(out_shardings_staged),
                           in_layouts=tuple(in_layouts_staged),
                           out_layouts=tuple(out_layouts_staged),
                           donated_invars=tuple(donated_invars_staged))
  assert len(new_params_staged['in_shardings']) == len(params_staged['jaxpr'].in_avals)
  assert len(new_params_staged['out_shardings']) == len(params_staged['jaxpr'].out_avals)
  assert len(new_params_staged['in_layouts']) == len(params_staged['jaxpr'].in_avals)
  assert len(new_params_staged['out_layouts']) == len(params_staged['jaxpr'].out_avals)
  return new_params_known, new_params_staged

