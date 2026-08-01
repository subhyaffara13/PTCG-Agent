
def lower_jaxpr_to_transform_func(
    jaxpr: jax_core.Jaxpr,
    aval: jax_core.AbstractValue,
    *,
    name: str,
    mosaic_grid_mapping: MosaicGridMapping,
    kernel_type: tpu_core.CoreType,
    forward_compatible: bool,
    backend: Any | None,
    dynamic_shape_replacement_fn: DynamicShapeReplacementFn,
    lowering_cache: dict[PallasLoweringCacheKey, func.FuncOp],
    dynamic_shape_env: LoweringDynamicShapeEnv | None = None,
) -> func.FuncOp:
  num_grid = len(mosaic_grid_mapping.grid_types)
  arg_types = [
      *mosaic_grid_mapping.grid_types,
      *mosaic_grid_mapping.scalar_prefetch_types,
  ]
  def body_func(*args):
    grid_indices, scalar_prefetch = split_list(args, [num_grid])
    jaxpr_indices = mosaic_grid_mapping.get_grid_indices(
        grid_indices, maybe_include_mapped_dims=True
    )
    arg_block_shapes = [
        *[()] * len(jaxpr_indices),
        *mosaic_grid_mapping.scalar_prefetch_block_shapes,
    ]

    lowering_context = LoweringContext(
        grid_sizes=cast(tuple[int, ...], mosaic_grid_mapping.grid),
        grid_names=mosaic_grid_mapping.grid_names,
        vmapped_dims=mosaic_grid_mapping.vmapped_dims,
        user_grid_indices=None,
        block_shapes=arg_block_shapes,
        name_stack=source_info_util.NameStack(),
        jax_mesh_context=mosaic_grid_mapping.mesh_info,
        kernel_type=kernel_type,
        traceback_caches=mlir.TracebackCaches(),
        forward_compatible=forward_compatible,
        backend=backend,
        dynamic_shape_replacement_fn=dynamic_shape_replacement_fn,
        lowering_cache=lowering_cache,
        dynamic_shape_env=dynamic_shape_env,
    )
    out = jaxpr_subcomp(lowering_context, jaxpr, *jaxpr_indices,
                        *scalar_prefetch)
    assert isinstance(aval, state.AbstractRef), aval
    # If we have an extended dtype, we need to add 0s for the block indices
    # for the remaining physical dtype.
    out += [ir_constant(0, mlir_type=_dtype_to_ir_type(jnp.int32))] * len(
        _get_aval_physical_dtype_shape(aval.inner_aval)
    )
    return out

  body_func.__name__ = name
  body: Any = func.FuncOp.from_py_func(*arg_types, name=name)(body_func)
  try:
    body.func_op.verify()
  except ir.MLIRError as e:
    raise error_handling.mlir_error_to_verification_error(e) from e
  return body.func_op

