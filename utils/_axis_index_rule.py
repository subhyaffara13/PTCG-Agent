
def _axis_index_rule(ctx: LoweringRuleContext, *, axis_name: Hashable):
  grid_names = ctx.lowering_context.grid_names
  if grid_names and axis_name in grid_names:
    # We are querying a named axis corresponding to a grid dimension.
    return _program_id_lowering_rule(ctx, axis=grid_names.index(axis_name))
  # We are querying a named axis corresponding to a mesh dimension.
  device_id = tpu.device_id()
  mesh_context = ctx.lowering_context.jax_mesh_context
  if mesh_context is None:
    raise ValueError("Mesh context is not set.")
  mesh_shape = mesh_context.mesh_shape
  axis_names = mesh_context.axis_names
  axis_index = axis_names.index(axis_name)
  axis_size = ir_constant(mesh_shape[axis_index])
  minor_divisor = ir_constant(math.prod(mesh_shape[axis_index + 1 :]))
  return arith.remsi(arith.divsi(device_id, minor_divisor), axis_size)


def _axis_index_rule(ctx: LoweringRuleContext, *, axis_name: Hashable):
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if axis_name == ctx.module_ctx.warp_axis_name:
      w_idx = mgpu.warp_idx(sync=True)
      i32 = ir.IntegerType.get_signless(32)
      return arith_dialect.remui(w_idx, _ir_constant(4, i32))
    raise ValueError(
        "Named axes can only refer to the warp axis name inside of core_map."
    )
  gpu_axis_names = ctx.module_ctx.axis_names
  jax_axis_names = getattr(ctx.module_ctx.mesh_info, "axis_names", ())
  if gpu_axis_names is None and not jax_axis_names:
    raise LookupError(
        "No axis names are available. Make sure you are using `pl.core_map`"
        " with a `plgpu.Mesh` or an appropriate JAX device mesh."
    )
  if axis_name not in itertools.chain(gpu_axis_names or (), jax_axis_names):
    raise LookupError(
        f"Axis {axis_name} does not refer to a GPU mesh axis (available axes:"
        f" {[*gpu_axis_names]}) or a JAX mesh axis (available axes:"
        f" {[*jax_axis_names]})"
    )
  if axis_name in jax_axis_names:
    jax_mesh = ctx.module_ctx.mesh_info
    assert jax_mesh is not None
    device_id = ctx.launch_ctx.device_id()
    jax_mesh_shape = jax_mesh.mesh_shape
    axis_index = jax_axis_names.index(axis_name)
    i32 = ir.IntegerType.get_signless(32)
    axis_size = _ir_constant(jax_mesh_shape[axis_index], i32)
    minor_divisor = _ir_constant(
        np.prod(jax_mesh_shape[axis_index + 1 :], dtype=np.int32), i32
    )
    return arith_dialect.remsi(arith_dialect.divsi(device_id, minor_divisor), axis_size)

  # We already checked that the axis is in scope and it wasn't a JAX mesh axis.
  assert gpu_axis_names is not None

  # We only deal with GPU axes from now on.
  axis_names = gpu_axis_names
  if axis_names.wg is not None and axis_name == axis_names.wg:
    return mgpu.warpgroup_idx(sync=True)

  if axis_name in axis_names.cluster:
    return arith_dialect.index_cast(
        ir.IntegerType.get_signless(32),
        gpu_dialect.cluster_block_id(
            gpu_dialect.Dimension(axis_names.cluster.index(axis_name))
        ),
    )
  block_ids = tuple(arith_dialect.index_cast(
          ir.IntegerType.get_signless(32),
          _block_id(ctx, dimension),
  ) for dimension in gpu_dialect.Dimension)
  return block_id_to_grid_id(ctx, block_ids, axis_name)


def _axis_index_rule(ctx: LoweringRuleContext, *, axis_name: Hashable):
  grid_names = ctx.context.grid_mapping.grid_names
  if grid_names is not None and axis_name in grid_names:
    # We are querying a named axis corresponding to a grid dimension.
    return _program_id_lowering_rule(ctx, axis=grid_names.index(axis_name))
  raise LookupError(f"Axis name {axis_name} not found in grid.")

