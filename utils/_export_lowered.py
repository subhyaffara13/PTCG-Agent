import itertools
import logging

def _export_lowered(
    lowered: stages.Lowered,
    jaxpr: core.ClosedJaxpr,
    fun_name: str,
    disabled_checks: Sequence[DisabledSafetyCheck] = (),
    _device_assignment_for_internal_jax2tf_use_only=None,
  ) -> Exported:
  version = config.jax_export_calling_convention_version.value
  if (version < minimum_supported_calling_convention_version or
      version > maximum_supported_calling_convention_version):
    raise ValueError(
      f"The requested export calling convention version {version} is outside the "
      f"range of supported versions [{minimum_supported_calling_convention_version}"
      f"..{maximum_supported_calling_convention_version}]")

  lowering = lowered._lowering
  _check_lowering(lowering)
  mlir_module = lowering.stablehlo()

  args_avals_flat, _ = tree_util.tree_flatten(lowered.in_avals)
  if "mut" in lowering.compile_args:
    if lowering.compile_args["mut"]: raise NotImplementedError
  if "kept_var_idx" in lowering.compile_args:
    module_kept_var_idx = tuple(sorted(lowering.compile_args["kept_var_idx"]))
  else:
    # For pmap
    module_kept_var_idx = tuple(range(len(args_avals_flat)))
  shape_poly_state = lowering.compile_args["shape_poly_state"]

  # Make a copy of mlir module as we should not mutate it
  # because it may be cached
  context = mlir.make_ir_context()
  with context, ir.Location.unknown(context):
    mlir_module = ir.Module.parse(mlir.module_to_bytecode(mlir_module))
  if (not all(core.is_constant_shape(a.shape) for a in args_avals_flat)
      or lowering.compile_args.get("ordered_effects", [])):
    mlir_module = _wrap_main_func(
        mlir_module, args_avals_flat, args_kwargs_tree=lowered.in_tree,
        has_platform_index_argument=shape_poly_state.has_platform_index_argument,
        module_kept_var_idx=module_kept_var_idx,
        serialization_version=version)

  with mlir_module.context:
    mlir_module_attrs = mlir_module.operation.attributes
    mlir_module_attrs["jax.uses_shape_polymorphism"] = (
        mlir.ir.BoolAttr.get(shape_poly_state.uses_dim_vars))

  # Shardy was used during lowering if we can find the Shardy mesh in the
  # module. Note that the mesh should have been lifted by the
  # `sdy-lift-inlined-meshes` pass in mlir.py.
  shardy_enabled = has_sdy_mesh(ir.SymbolTable(mlir_module.operation),
                                mlir_module)

  mlir_module_serialized = _module_to_bytecode(mlir_module)

  # Figure out the result types and shapes
  if "global_out_avals" in lowering.compile_args:
    # This is currently the case for pjit
    out_avals_flat = lowering.compile_args["global_out_avals"]
  else:
    out_avals_flat = lowered.compile_args["out_avals"]  # pyrefly: ignore[missing-attribute]

  # Log and then check the module.
  if logger.isEnabledFor(logging.DEBUG):
    logmsg = (f"fun_name={fun_name} version={version} "
              f"lowering_platforms={lowering._platforms} "  # pyrefly: ignore[missing-attribute]
              f"disabled_checks={disabled_checks}")
    logger.debug("Exported JAX function: %s\n", logmsg)
    logger.debug(mlir.dump_module_message(mlir_module, "export"))
    logger.debug(
        "Size of mlir_module_serialized: %d byte",
        len(mlir_module_serialized),
    )

  _check_module(mlir_module,
                disabled_checks=disabled_checks,
                shardy_enabled=shardy_enabled)

  ordered_effects = tuple(lowering.compile_args["ordered_effects"])
  unordered_effects = tuple(lowering.compile_args["unordered_effects"])

  nr_devices = lowering.compile_args["num_devices"]

  all_in_shardings = expand_in_shardings(lowering.compile_args["in_shardings"],
                                         module_kept_var_idx,
                                         len(args_avals_flat))

  cur_mesh = None
  if config.use_shardy_partitioner.value:
    for sharding in itertools.chain(
        all_in_shardings, lowering.compile_args["out_shardings"]
    ):
      if isinstance(sharding, sharding_impls.NamedSharding):
        cur_mesh = sharding.mesh
        break
    if cur_mesh is not None and isinstance(cur_mesh, mesh_lib.Mesh):
      cur_mesh = cur_mesh.abstract_mesh

  in_named_shardings = tuple(
    to_named_sharding_with_abstract_mesh(s, aval, cur_mesh)
    for s, aval in zip(all_in_shardings, args_avals_flat))

  out_named_shardings = tuple(
    to_named_sharding_with_abstract_mesh(s, aval, cur_mesh)
    for s, aval in zip(lowering.compile_args["out_shardings"], out_avals_flat))

  device_assignment = lowering._device_list  # pyrefly: ignore[missing-attribute]
  if _device_assignment_for_internal_jax2tf_use_only is not None:
    _device_assignment_for_internal_jax2tf_use_only[0] = device_assignment

  def _get_exported_vjp(exp_primal: Exported) -> Exported:
    # Turn the primal jaxpr into a function, in preparation for exporting
    # the VJP. Note that jaxpr_as_fun produces a function with flat arguments
    assert(jaxpr is not None)  # None only when the lowered was created outside JAX
    fun_jax = core.jaxpr_as_fun(jaxpr)
    assert exp_primal._has_named_shardings
    fun_vjp_jax, vjp_in_avals = _get_vjp_fun(
        fun_jax,
        in_tree=exp_primal.in_tree,
        in_avals=exp_primal.in_avals,
        has_named_shardings=True,
        in_shardings_hlo=(None,) * len(exp_primal._in_named_shardings),
        out_shardings_hlo=(None,) * len(exp_primal._out_named_shardings),
        in_named_shardings=exp_primal._in_named_shardings,
        out_named_shardings=exp_primal._out_named_shardings,
        out_avals=exp_primal.out_avals,
        device_assignment=device_assignment,
        apply_jit=True,
        flat_primal_fun=True,
        mesh=cur_mesh)
    return export(fun_vjp_jax,
                  platforms=exp_primal.platforms,
                  disabled_checks=exp_primal.disabled_safety_checks)(*vjp_in_avals)

  return Exported(
      fun_name=fun_name,
      in_tree=lowered.in_tree,
      out_tree=lowered.out_tree,
      in_avals=tuple(args_avals_flat),
      out_avals=tuple(out_avals_flat),
      _has_named_shardings=True,
      _in_named_shardings=in_named_shardings,
      _out_named_shardings=out_named_shardings,
      in_shardings_hlo=(None,) * len(in_named_shardings),
      out_shardings_hlo=(None,) * len(out_named_shardings),

      nr_devices=nr_devices,
      platforms=lowering._platforms,  # pyrefly: ignore[missing-attribute]
      ordered_effects=ordered_effects,
      unordered_effects=unordered_effects,
      disabled_safety_checks=tuple(disabled_checks),
      mlir_module_serialized=mlir_module_serialized,
      module_kept_var_idx=module_kept_var_idx,
      uses_global_constants=shape_poly_state.uses_dim_vars,
      calling_convention_version=version,
      _get_vjp=_get_exported_vjp)

