
def _mosaic_gpu_lowering_rule(
    ctx,
    *args,
    module,
    out_types,
    inout_types,
    input_output_aliases: tuple[tuple[int, int], ...] = (),
    use_custom_barrier: bool = False,
):
  axis_context = ctx.module_context.axis_context
  replica_ids = []
  if is_multi_device_module := _has_communication(module):
    # Those checks are trying to ensure that the logical device ids are
    # consistent with the NVSHMEM PE ids that Mosaic will be using for
    # communication. Any divergence here would require us to implement a logical
    # to physical translation, which is currently not implemented.
    if isinstance(axis_context, sharding_impls.SPMDAxisContext):
      mesh = axis_context.mesh
      if isinstance(mesh, mesh_lib.Mesh):
        replica_ids = mesh.device_ids.ravel()
        # Skip the check for AbstractMesh
        if not np.array_equal(mesh.device_ids.ravel(), np.arange(mesh.size)):
          raise NotImplementedError(
              "Mosaic GPU only supports meshes with device ordering that follows"
              f" row-major device ids. Got: {mesh.device_ids.ravel()} device ids."
          )
    elif isinstance(axis_context, sharding_impls.ShardingContext):
      if axis_context.num_devices != 1:
        raise NotImplementedError(
            "Mosaic GPU only supports single-device meshes in ShardingContext."
            f" Got: {axis_context.num_devices} devices."
        )
    else:
      raise NotImplementedError(f"Unsupported sharding context: {axis_context}")

  if inout_types:
    if input_output_aliases:
      raise ValueError(
          "input_output_aliases and inout_types are mutually exclusive"
      )
    num_inputs = len(ctx.avals_in)
    num_outputs = len(ctx.avals_out)
    input_output_aliases = tuple(
        (num_inputs - 1 - i, num_outputs - 1 - i)
        for i in range(len(inout_types))
    )
  assert len(ctx.avals_in) == len(args)
  assert len(ctx.avals_out) == len(out_types) + len(inout_types)
  module = _run_serde_pass(
      module,
      serialize=True,
      ir_version=FWD_COMPAT_IR_VERSION if ctx.is_forward_compat() else None,
  )
  bytecode_buffer = io.BytesIO()
  module.operation.write_bytecode(bytecode_buffer, desired_version=0)
  module_asm = bytecode_buffer.getvalue()
  kernel_id = hashlib.sha256(module_asm).digest()
  # Note that this is technically only a half measure. Someone might load a
  # compiled module with a hash collision from disk. But that's so unlikely with
  # SHA256 that it shouldn't be a problem.
  if (kernel_text := KNOWN_KERNELS.get(kernel_id, None)) is not None:
    if kernel_text != module_asm:
      raise RuntimeError("Kernel hash collision!")
  else:
    KNOWN_KERNELS[kernel_id] = module_asm

  backend_config: dict[str, ir.Attribute] = dict(
      kernel_hash=ir.StringAttr.get(kernel_id),
      module=ir.StringAttr.get(module_asm),
      use_custom_barrier=ir.BoolAttr.get(use_custom_barrier),
      uses_xla_collective_metadata=ir.BoolAttr.get(
          launch_context.uses_collective_metadata(module)
      ),
  )

  # If NVSHMEM is available it will be used by default, otherwise we will use
  # collective metadata.
  if is_multi_device_module and (
      is_single_process_multi_device_topology() or not is_nvshmem_available()
  ):
    backend_config["xla_replica_ids"] = ir.StringAttr.get(
        ",".join(map(str, replica_ids))
    )

    if launch_context.MULTIMEM_ARGS_ATTR in module.operation.attributes:
      multimem_args = np.array(
          ir.DenseIntElementsAttr(
              module.operation.attributes[launch_context.MULTIMEM_ARGS_ATTR]
          ),
          dtype=bool,
      )
      backend_config["multimem_parameters"] = ir.StringAttr.get(
          ",".join(map(str, map(int, multimem_args)))
      )

  result_types, _ = mlir.ir_tree_registry.flatten([
      mlir.aval_to_ir_type(ctx.module_context, aval) for aval in ctx.avals_out
  ])
  return mlir.custom_call(
      call_target_name="mosaic_gpu_v2",
      result_types=result_types,
      operands=args,
      operand_layouts=[list(reversed(range(a.ndim))) for a in ctx.avals_in],
      result_layouts=[list(reversed(range(a.ndim))) for a in ctx.avals_out],
      backend_config=backend_config,
      operand_output_aliases=dict(input_output_aliases),
      api_version=4,
  ).results

