
def _partial_eval_jaxpr_custom_rule(
    saveable: Callable[..., pe.RematCases_], unks_in: Sequence[bool],
    inst_in: Sequence[bool], eqn: core.JaxprEqn
) -> tuple[core.JaxprEqn, core.JaxprEqn, Sequence[bool], Sequence[bool],
           list[core.Var]]:
  jaxpr, mesh = eqn.params['jaxpr'], eqn.params['mesh']
  check_vma, manual_axes = eqn.params['check_vma'], eqn.params['newly_manual_axes']
  with (_extend_axis_env(mesh, manual_axes), config._check_vma(check_vma),
        use_abstract_mesh(_as_manual_mesh(mesh, manual_axes))):
    jaxpr_known, jaxpr_staged, unks_out, inst_out, num_res = \
        pe.partial_eval_jaxpr_custom(jaxpr, unks_in, inst_in, False, False, saveable)
  num_out_primals = len(jaxpr_known.outvars) - num_res
  in_fwd = pe._jaxpr_forwarding(jaxpr_known)[num_out_primals:]
  out_binders_known, _ = partition_list(unks_out, eqn.outvars)
  out_vars, res_vars = split_list(jaxpr_known.outvars, [num_out_primals])
  idx_map = {id(v): i for i, (v, b) in enumerate(zip(out_vars, out_binders_known))
             if not isinstance(b, core.DropVar)}
  out_fwd = [idx_map.get(id(v)) for v in res_vars]
  which = [f1 is None and f2 is None for f1, f2 in zip(in_fwd, out_fwd)]
  mesh = eqn.params['mesh']
  with (_extend_axis_env(mesh, manual_axes),
        use_abstract_mesh(_as_manual_mesh(mesh, manual_axes)),
        config._check_vma(check_vma)):
    jaxpr_known = pe.prune_jaxpr_outputs(jaxpr_known, [True] * num_out_primals + which)
    jaxpr_known, jaxpr_staged = _add_reshapes(which, jaxpr_known, jaxpr_staged)
  jaxpr_known = core.remove_named_axis_effects(jaxpr_known, mesh.axis_names)
  jaxpr_staged = core.remove_named_axis_effects(jaxpr_staged, mesh.axis_names)
  ins_known, _ = partition_list(unks_in, eqn.invars)
  _, ins_staged = partition_list(inst_in, eqn.invars)
  _, out_binders_staged = partition_list(inst_out, eqn.outvars)
  nv = core.gensym()
  all_names = _all_newly_manual_mesh_names(mesh, manual_axes)
  lns = lambda a: a.nospec(mesh, check_vma, all_names)
  residuals, staged_in_res_specs = unzip2(
      [(nv(unshard_aval(mesh, check_vma, (rn := lns(var.aval)), var.aval)), rn)
       for var, w in zip(jaxpr_staged.invars[:num_res], which) if w])
  out_res_specs_known = [var.aval.nospec(mesh, check_vma, all_names)  # pyrefly: ignore[missing-attribute]
                         for var, w in zip(res_vars, which) if w]
  params_known, params_staged = _pe_custom_params(
      unks_in, inst_in, map(op.not_, unks_out), inst_out, in_fwd, out_fwd,
      out_res_specs_known, staged_in_res_specs,
      dict(eqn.params, jaxpr=jaxpr_known), dict(eqn.params, jaxpr=jaxpr_staged))
  eqn_known = pe.new_jaxpr_eqn(ins_known, [*out_binders_known, *residuals],
                               eqn.primitive, params_known, jaxpr_known.effects,
                               eqn.source_info, eqn.ctx)
  full_res = subs_list2(in_fwd, out_fwd, ins_known, out_binders_known, residuals)
  eqn_staged = pe.new_jaxpr_eqn([*full_res, *ins_staged], out_binders_staged,
                                eqn.primitive, params_staged,
                                jaxpr_staged.effects, eqn.source_info, eqn.ctx)
  assert len(eqn_staged.invars) == len(jaxpr_staged.invars)
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is core.Var and not inst]
  new_inst += [out_binders_known[f] for f in {i for i in out_fwd if i is not None}]
  return eqn_known, eqn_staged, unks_out, inst_out, new_inst + list(residuals)

