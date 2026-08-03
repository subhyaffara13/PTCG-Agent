from typing import Any

def lower_sharding_computation(
    closed_jaxpr: core.ClosedJaxpr,
    api_name: str,
    fun_name: str,
    in_shardings: Sequence[MaybeSharding],
    out_shardings: Sequence[MaybeSharding],
    in_layouts: MaybeLayout,
    out_layouts: MaybeLayout,
    donated_invars: Sequence[bool],
    *,
    keep_unused: bool,
    context_mesh: Mesh | AbstractMesh,
    compiler_options_kvs: tuple[tuple[str, Any], ...],
    lowering_platforms: tuple[str, ...] | None,
    lowering_parameters: mlir.LoweringParameters,
    pgle_profiler: profiler.PGLEProfiler | None,
) -> MeshComputation:
  all_args_info = AllArgsInfo(closed_jaxpr.in_avals, closed_jaxpr.jaxpr._debug_info)

  closed_jaxpr, donated_invars, kept_var_idx = _dce_jaxpr(
      closed_jaxpr, keep_unused, donated_invars)
  in_shardings = tuple(s for i, s in enumerate(in_shardings) if i in kept_var_idx)
  in_layouts = tuple(l for i, l in enumerate(in_layouts) if i in kept_var_idx)

  (closed_jaxpr, inout_aliases, mut, in_shardings, in_layouts,
   donated_invars, out_shardings, out_layouts) = _discharge_refs_jaxpr(
       closed_jaxpr, in_shardings, in_layouts, donated_invars, out_shardings,
       out_layouts)

  jaxpr = closed_jaxpr.jaxpr
  global_in_avals = closed_jaxpr.in_avals
  global_out_avals = closed_jaxpr.out_avals

  if lowering_parameters.hoist_constants_as_args:
    (const_args, global_in_avals, in_shardings, in_layouts, donated_invars,
     kept_var_idx, inout_aliases, mut, all_args_info) = hoist_constants_as_args(
         closed_jaxpr, global_in_avals, in_shardings, in_layouts,
         donated_invars, kept_var_idx, inout_aliases, mut, all_args_info)
  else:
    const_args = []

  # If layout is propagated, then set the out_layout in the top module to AUTO
  # so that XLA can override the entry_computation_layout. The propagated
  # layout will be set via a custom call.
  out_layouts_via_prop = get_out_layouts_via_propagation(closed_jaxpr)
  out_layouts = tuple(Layout.AUTO if p is not None else o
                      for o, p in safe_zip(out_layouts, out_layouts_via_prop))

  assert len(out_shardings) == len(out_layouts) == len(global_out_avals), (
      len(out_shardings), len(out_layouts), len(global_out_avals))

  context_mesh = _get_context_mesh(context_mesh)

  # Device assignment across all inputs, outputs and shardings inside jaxpr
  # should be the same.
  unique_intermediate_shardings = util.stable_unique(
      dispatch.get_intermediate_shardings(jaxpr))
  unique_const_shardings = util.stable_unique(in_shardings[:len(const_args)])
  unique_in_shardings = util.stable_unique(in_shardings[len(const_args):])
  unique_out_shardings = util.stable_unique(out_shardings)
  backend, device_assignment, num_devices = _get_and_check_device_assignment(
      it.chain(
          ((i, stages.MismatchType.ARG_SHARDING, None) for i in unique_in_shardings),
          ((c, stages.MismatchType.CONST_SHARDING, None) for c in unique_const_shardings),
          ((o, stages.MismatchType.OUT_SHARDING, None) for o in unique_out_shardings),
          ((js, stages.MismatchType.SHARDING_INSIDE_COMPUTATION, source_info)
           for js, source_info in unique_intermediate_shardings)),
      context_mesh)
  unique_intermediate_shardings = [js for js, _ in unique_intermediate_shardings]
  unique_in_shardings = unique_in_shardings | unique_const_shardings  # pyrefly: ignore[unsupported-operation]
  del unique_const_shardings

  prim_requires_devices = dispatch.jaxpr_has_prim_requiring_devices(jaxpr)

  if device_assignment is None:
    if lowering_platforms is None:
      raise ValueError(
          "Passing lowering_platforms via jax.export or"
          " jit(f).trace(*args).lower(lowering_platforms=...) is required when"
          " only AbstractMesh exists in a jitted computation. Got context"
          f" mesh: {context_mesh}")
    if prim_requires_devices:
      raise ValueError(
          "AbstractMesh cannot be used when jaxpr contains primitives that"
          " require devices to be present during lowering.")

  # For device_assignment == 1, this doesn't matter.
  if device_assignment is not None and len(device_assignment) > 1:
    rep_gs = GSPMDSharding.get_replicated(device_assignment)
    in_shardings = tuple(
        rep_gs if (isinstance(s, UnspecifiedValue) and
                   aval is not core.abstract_token and aval.ndim == 0)
        else s for s, aval in zip(in_shardings, global_in_avals))

  for a in global_out_avals:
    if (a is not core.abstract_token and not a.sharding.mesh.empty and
        a.sharding.mesh.are_all_axes_explicit and
        device_assignment is not None and
        len(device_assignment) != a.sharding.mesh.size):
      raise ValueError(
          f"Length of device assignment {len(device_assignment)} is not equal"
          f" to the size of the mesh {a.sharding.mesh.size} of aval"
          f" {a.str_short(True, True)}. Please enter your `jit` into a mesh"
          " context via `jax.set_mesh`.")

  # TODO(parkers): One _raw_platform has been unified with platform,
  # change this back to just read platform.
  platforms = lowering_platforms or (
      getattr(backend, "_raw_platform", backend.platform),)

  device_list = _create_device_list(device_assignment)
  transfer_mem_kind_in_jaxpr = jaxpr_transfer_mem_kinds(jaxpr)

  committed = bool(
      not context_mesh.empty
      or num_devices > 1
      or any(not isinstance(s, UnspecifiedValue) for s in it.chain(
          unique_in_shardings, unique_out_shardings,
          unique_intermediate_shardings))
      or transfer_mem_kind_in_jaxpr
  )

  all_default_mem_kind = are_all_shardings_default_mem_kind(
      it.chain(unique_in_shardings, unique_out_shardings,
               unique_intermediate_shardings, transfer_mem_kind_in_jaxpr))

  if all_default_mem_kind:
    propagated_out_mem_kinds = (None,) * len(global_out_avals)
  else:
    propagated_out_mem_kinds = tuple(
        core.mem_space_to_kind(o.memory_space) for o in closed_jaxpr.out_avals)

  out_shardings = _concretize_abstract_out_shardings(
      out_shardings, global_out_avals, device_assignment,
      propagated_out_mem_kinds)

  global_in_avals = [core.update_aval_with_sharding(a, sh)
                     if isinstance(a, core.ShapedArray) else a
                     for a, sh in zip(global_in_avals, in_shardings)]
  global_out_avals = [core.update_aval_with_sharding(a, sh)
                      if isinstance(a, core.ShapedArray) else a
                      for a, sh in zip(global_out_avals, out_shardings)]

  ############################ Build up the stableHLO ######################

  abstract_mesh = None
  if prim_requires_devices:
    assert device_list is not None
    for sharding in it.chain(unique_in_shardings, unique_out_shardings,
                             unique_intermediate_shardings):
      if isinstance(sharding, NamedSharding):
        if (abstract_mesh is not None and
            abstract_mesh != sharding.mesh.abstract_mesh):
          raise ValueError(
              "mesh should be the same across the entire program. Got mesh"
              f" shape for one sharding {abstract_mesh} and"
              f" {sharding.mesh.abstract_mesh} for another")
        abstract_mesh = sharding.mesh.abstract_mesh

  semantic_in_shardings = SemanticallyEqualShardings(
      in_shardings, global_in_avals)
  semantic_out_shardings = SemanticallyEqualShardings(
      out_shardings, global_out_avals)

  jaxpr_util.maybe_dump_jaxpr_to_file(fun_name, closed_jaxpr.jaxpr)
  module_name = util.wrap_name(api_name, fun_name)

  (module, keepalive, host_callbacks, unordered_effects, ordered_effects,
   tuple_args, shape_poly_state) = _cached_lowering_to_hlo(
       closed_jaxpr, module_name, backend,
       len(const_args), tuple(global_in_avals),
       semantic_in_shardings, semantic_out_shardings,
       in_layouts, out_layouts, num_devices,
       tuple(device_list) if prim_requires_devices else None,  # pyrefly: ignore[bad-argument-type]
       donated_invars, all_default_mem_kind, inout_aliases,
       propagated_out_mem_kinds, platforms,
       lowering_parameters=lowering_parameters,
       abstract_mesh=abstract_mesh)

  # backend and device_assignment is passed through to MeshExecutable because
  # if keep_unused=False and all in_shardings are pruned, then there is no way
  # to get the device_assignment and backend. So pass it to MeshExecutable
  # because we calculate the device_assignment and backend before in_shardings,
  # etc are pruned.
  return MeshComputation(
      module_name,
      module,
      const_args,
      donated_invars,
      platforms,
      compiler_options_kvs,
      device_list,
      global_in_avals=global_in_avals,
      global_out_avals=global_out_avals,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      tuple_args=tuple_args,
      unordered_effects=unordered_effects,
      ordered_effects=ordered_effects,
      host_callbacks=host_callbacks,
      keepalive=keepalive,
      kept_var_idx=kept_var_idx,
      mut=mut,
      backend=backend,
      num_devices=num_devices,
      committed=committed,
      in_layouts=in_layouts,
      out_layouts=out_layouts,
      shape_poly_state=shape_poly_state,
      all_args_info=all_args_info,
      pgle_profiler=pgle_profiler,
      intermediate_shardings=unique_intermediate_shardings,
      context_mesh=context_mesh)

