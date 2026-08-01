
def refine_polymorphic_shapes(module: ir.Module) -> ir.Module:
  """Refines the polymorphic shapes inside a module.

  Given a module with static input shapes, but using dynamic shapes due to
  shape polymorphism, runs shape refinement to resolve all the dynamic shapes.
  Then verifies that there are no more dynamic shapes in the module.
  """
  try:
    refine_polymorphic_shapes = partial(_jax.mlir.refine_polymorphic_shapes,
            mlir_module=module_to_bytecode(module),
            enable_shape_assertions=True,
            validate_static_shapes=True)
    refined_module_str = refine_polymorphic_shapes(
        enable_shardy=config.use_shardy_partitioner.value)
  except Exception as e:
    raise ValueError(
        "Error refining shapes. " +
        dump_module_message(module, "before_refine_polymorphic_shapes")) from e

  context = make_ir_context()
  with context:
    return ir.Module.parse(refined_module_str)

