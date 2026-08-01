
def closed_call_partial_eval_custom_rule(
    jaxpr_param_name: str, params_updater: ParamsUpdater2,
    saveable: Callable[..., RematCases_], unks_in: list[bool], inst_in: list[bool],
    eqn: JaxprEqn, *, res_aval: ResAvalUpdater = _default_res_aval_updater,
  ) -> tuple[JaxprEqn, JaxprEqn, Sequence[bool], Sequence[bool], list[Var]]:
  # TODO(sharadmv,mattjj): dedup this rule with call_partial_eval_custom_rule.
  disallow_output_fwds = tuple(isinstance(v, DropVar) for v in eqn.outvars)
  # TODO(mattjj): this is just for pjit... but let's delete all this code
  from jax._src.sharding_impls import UNSPECIFIED  # pyrefly: ignore[missing-import]
  in_shardings, in_layouts = eqn.params.get('in_shardings'), eqn.params.get('in_layouts')
  if in_shardings is not None:
    assert in_layouts is not None
    disallow_input_fwds = tuple(s is not UNSPECIFIED or l is not None
                                for s, l in zip(in_shardings, in_layouts))
  else:
    disallow_input_fwds = (False,) * len(unks_in)
  jaxpr_known, jaxpr_staged, unks_out, inst_out, num_res_ref, num_res_val, in_fwd, out_fwd = \
      _closed_jaxpr_partial_eval_custom_cached(
          eqn.params[jaxpr_param_name], (*unks_in,), (*inst_in,),
          disallow_input_fwds, disallow_output_fwds, saveable)
  num_res = num_res_ref + num_res_val
  out_binders_known, _ = partition_list(unks_out, eqn.outvars)
  ins_known, _ = partition_list(unks_in, eqn.invars)
  _, ins_staged = partition_list(inst_in, eqn.invars)
  _, out_binders_staged = partition_list(inst_out, eqn.outvars)
  params_known = {**eqn.params, jaxpr_param_name: jaxpr_known}
  params_staged = {**eqn.params, jaxpr_param_name: jaxpr_staged}
  params_known, params_staged = params_updater(
      unks_in, inst_in, map(op.not_, unks_out), inst_out,
      sum(fin is fout is None for fin, fout in zip(in_fwd, out_fwd)),
      num_res, params_known, params_staged)
  res_val_binders, res_ref_binders = split_list(
      [Var(res_aval(params_known, v))
       for v in jaxpr_staged.in_avals[:num_res]], [num_res_val])
  res_val_binders = [v for v, fin, fout in zip(res_val_binders, in_fwd, out_fwd)
                     if fin is fout is None]
  res_val_binders_ = iter(res_val_binders)
  res_val_vars = [out_binders_known[fout] if fout is not None else
                  ins_known[fin] if fin is not None else
                  next(res_val_binders_) for fin, fout in zip(in_fwd, out_fwd)]
  assert next(res_val_binders_, None) is None
  eqn_known = new_jaxpr_eqn(
      [*ins_known, *res_ref_binders], [*out_binders_known, *res_val_binders],
      eqn.primitive, params_known,
      core.eqn_effects(jaxpr_known, [*ins_known, *res_ref_binders]),
      eqn.source_info, eqn.ctx)
  eqn_staged = new_jaxpr_eqn(
      [*res_val_vars, *res_ref_binders, *ins_staged], out_binders_staged,
      eqn.primitive, params_staged,
      core.eqn_effects(jaxpr_staged, [*res_val_vars, *res_ref_binders, *ins_staged]),
      eqn.source_info, eqn.ctx)
  assert len(eqn_staged.invars) == len(jaxpr_staged.in_avals)
  assert len(ins_known) + len(res_ref_binders) == len(jaxpr_known.jaxpr.invars)
  assert len(ins_staged) + len(res_ref_binders) + len(res_val_vars) == len(jaxpr_staged.jaxpr.invars)
  assert len(out_binders_known) + len(res_val_binders) == len(jaxpr_known.jaxpr.outvars)
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is Var and not inst]
  new_vars = [*new_inst, *res_val_vars, *res_ref_binders]
  return eqn_known, eqn_staged, unks_out, inst_out, new_vars  # pyrefly: ignore[bad-return]

