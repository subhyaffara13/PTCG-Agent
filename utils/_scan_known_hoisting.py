
def _scan_known_hoisting(jaxpr_known, known_consts, num_res):
  # To disable:
  # return jaxpr_known, known_consts, [False] * num_res, []

  consts = [pe.PartialVal.unknown(a) if isinstance(a := typeof(c), AbstractRef)
            else pe.PartialVal.known(c) for c in known_consts]
  others = _map(pe.PartialVal.unknown, jaxpr_known.in_avals[len(consts):])
  num_known_outs = len(jaxpr_known.out_avals) - num_res
  with source_info_util.reset_name_stack():
    jaxpr_known_, pvals_out, new_known_consts = pe.trace_to_jaxpr_nounits(
        lu.wrap_init(core.jaxpr_as_fun(jaxpr_known),
                     debug_info=jaxpr_known.jaxpr.debug_info),
        consts + others, instantiate=[True] * num_known_outs + [False] * num_res)
  jaxpr_known = pe.close_jaxpr(pe.convert_constvars_jaxpr(jaxpr_known_))
  res_pvals = pvals_out[num_known_outs:]
  which_hoisted = [pval.is_known() for pval in res_pvals]
  hoisted_res = [pval.get_known() for pval in res_pvals if pval.is_known()]
  mut_consts = [c for c in known_consts if isinstance(typeof(c), AbstractRef)]
  return jaxpr_known, [*new_known_consts, *mut_consts], which_hoisted, hoisted_res

