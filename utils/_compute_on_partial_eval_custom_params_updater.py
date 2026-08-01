
def _compute_on_partial_eval_custom_params_updater(
    unks_in: Sequence[bool], inst_in: Sequence[bool],
    kept_outs_known: Sequence[bool], kept_outs_staged: Sequence[bool],
    num_res_out: int, num_res_in: int, params_known, params_staged):
  # prune inputs to jaxpr_known according to unks_in
  _, out_memory_spaces_known = pe.partition_list(
      kept_outs_known, params_known['out_memory_spaces'])
  new_params_known = dict(
      params_known,
      out_memory_spaces=(*out_memory_spaces_known,
                         *[core.MemorySpace.Device] * num_res_out),
  )
  assert (len(new_params_known['out_memory_spaces']) ==
          len(params_known['jaxpr'].out_avals))

  # added num_res new inputs to jaxpr_staged, and pruning according to inst_in
  _, out_memory_spaces_staged = pe.partition_list(
      kept_outs_staged, params_staged['out_memory_spaces'])
  new_params_staged = dict(
      params_staged,
      out_memory_spaces=tuple(out_memory_spaces_staged),
  )
  assert (len(new_params_staged['out_memory_spaces']) ==
          len(params_staged['jaxpr'].out_avals))
  return new_params_known, new_params_staged

