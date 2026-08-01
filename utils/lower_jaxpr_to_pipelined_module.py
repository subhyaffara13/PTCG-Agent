
def lower_jaxpr_to_pipelined_module(
    lowering_context: mlir.LoweringRuleContext,
    grid_mapping: pallas_core.GridMapping,
    jaxpr: jax_core.Jaxpr,
    *,
    dimension_semantics: Sequence[tpu_core.DimensionSemantics] | None,
    kernel_type: tpu_core.CoreType,
    mesh: mesh_lib.Mesh | None = None,
    dynamic_shape_replacement_enabled: bool = False,
    fuse_transposed_lhs_in_matmul: bool = False,
) -> ir.Module:
  module = ir.Module.create()
  lower_jaxpr_into_pipelined_module(
      lowering_context,
      module,
      grid_mapping,
      jaxpr,
      name=mlir.sanitize_name(jaxpr.debug_info.func_name),
      dimension_semantics=dimension_semantics,
      kernel_type=kernel_type,
      mesh=mesh,
      dynamic_shape_replacement_enabled=dynamic_shape_replacement_enabled,
      fuse_transposed_lhs_in_matmul=fuse_transposed_lhs_in_matmul,
  )
  return module

