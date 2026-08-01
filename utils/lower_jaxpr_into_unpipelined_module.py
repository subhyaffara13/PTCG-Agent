
def lower_jaxpr_into_unpipelined_module(
    lowering_context: mlir.LoweringRuleContext,
    module: ir.Module,
    jaxpr: jax_core.Jaxpr,
    *,
    name: str,
    pallas_mesh: pallas_core.Mesh,
    jax_mesh: mesh_lib.Mesh | None,
    dynamic_shape_replacement_enabled: bool = False,
    num_scratch: int,
    needs_layout_passes: bool = False,
    fuse_transposed_lhs_in_matmul: bool = False,
) -> None:
  if pallas_mesh is None:
    raise ValueError("Mesh must be provided.")
  if dynamic_shape_replacement_enabled:
    raise NotImplementedError(
        "Dynamic shape replacement is not supported for unpipelined lowering."
    )
  backend = lowering_context.module_context.get_backend(optional=True)
  # NOTE: We should bump this periodically
  if backend is not None and is_cloud_tpu_older_than(2026, 4, 1, backend):
    platform_version = xla_bridge.get_backend().platform_version
    raise RuntimeError(
        "Pallas TPU requires a libtpu version that's at most a month old. Found"
        f" version string:\n{platform_version}"
    )
  sym_tab = ir.SymbolTable(module.operation)
  cache = lowering_context.module_context.pallas_lowering_cache
  mesh_shape, dimension_semantics = _get_mesh_shape_and_semantics(pallas_mesh)
  num_grid = len(mesh_shape)
  mesh_index_types = [jax_core.ShapedArray((), jnp.int32)] * len(mesh_shape)
  arg_jax_types = [*mesh_index_types, *[v.aval for v in jaxpr.invars]]
  arg_mlir_types = [
      aval_to_ir_type(lambda x: x, v, kernel_type=pallas_mesh.core_type)
      for v in arg_jax_types
  ]

  def ctx_factory(mesh_indices):
    return UnpipelinedLoweringContext.from_mesh(
        mesh_shape,
        jaxpr,
        jax_mesh,
        core_type=pallas_mesh.core_type,
        forward_compatible=lowering_context.is_forward_compat(),
        backend=backend,
        needs_layout_passes=needs_layout_passes,
        mesh_indices=mesh_indices,
        fuse_transposed_lhs_in_matmul=fuse_transposed_lhs_in_matmul,
        lowering_cache=cache,
    )

  with ir.InsertionPoint(module.body):
    func_op = _lower_jaxpr_to_func_common(
        jaxpr,
        name=name,
        arg_types=arg_mlir_types,
        num_grid=num_grid,
        get_jaxpr_indices=lambda idx: idx,
        ctx_factory=ctx_factory,
        dynamic_shape_replacement_enabled=False,
        core_type=pallas_mesh.core_type,
    )

  func_op.attributes["tpu.core_type"] = ir.Attribute.parse(
      f"#tpu.core_type<{pallas_mesh.core_type}>"
  )
  module.body.append(func_op)
  assert name not in sym_tab, f"Function name {name} already exists in symbol table."
  sym_tab.insert(func_op)
  grid = tuple(m[1] for m in mesh_shape)
  func_op.attributes["iteration_bounds"] = ir.DenseI64ArrayAttr.get(grid)
  func_op.attributes["scalar_prefetch"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), 0)
  func_op.attributes["scratch_operands"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), num_scratch)
  func_op.attributes["dimension_semantics"] = _get_dimension_semantics(
      dimension_semantics
  )

  # TODO(sharadmv): Relax compiler checks to allow for no windowing.
  # Set up trivial windowing.
  window_params = []
  for v in jaxpr.invars[:-num_scratch] if num_scratch > 0 else jaxpr.invars:
    aval = v.aval
    assert isinstance(aval, state.AbstractRef), aval
    block_memory_space = aval.memory_space
    if block_memory_space is None:
      block_memory_space = pallas_core.MemorySpace.ANY
    tpu_memory_space = tpu_core.memory_space_to_tpu_memory_space(
        block_memory_space, pallas_mesh.core_type
    )

    # TODO(slebedev): Update the SparseCore compiler to allow this.
    is_sc = pallas_mesh.core_type in (
        tpu_core.CoreType.SC_SCALAR_SUBCORE,
        tpu_core.CoreType.SC_VECTOR_SUBCORE,
    )
    if not is_sc and (
        tpu_memory_space is ANY
        or tpu_memory_space == tpu_core.MemorySpace.HBM
        or tpu_memory_space == SEMAPHORE
    ):
      window_params.append(ir.DictAttr.get())
      continue

    rank = len(aval.shape)
    exprs = [ir.AffineConstantExpr.get(0)] * rank
    affine_map = ir.AffineMap.get(len(grid), 0, exprs)
    block_params = dict[str, ir.Attribute](
        transform_indices=ir.AffineMapAttr.get(affine_map),
    )
    window_params.append(ir.DictAttr.get(block_params))
  func_op.attributes["window_params"] = ir.ArrayAttr.get(window_params)

