from typing import Any, Callable

def _lower_jaxpr_to_func_common(
    jaxpr: jax_core.Jaxpr,
    *,
    name: str,
    arg_types: list[ir.Type],
    num_grid: int,
    get_jaxpr_indices: Callable[[list[ir.Value]], list[ir.Value]],
    ctx_factory: Callable[[list[ir.Value]], LoweringContext],
    dynamic_shape_replacement_enabled: bool = False,
    core_type: tpu_core.CoreType | None = None,
) -> func.FuncOp:
  def body_func(*args):
    grid_indices = list(args[:num_grid])
    other_args = list(args[num_grid:])

    jaxpr_indices = get_jaxpr_indices(grid_indices)
    lowering_context = ctx_factory(jaxpr_indices)

    return jaxpr_subcomp(lowering_context, jaxpr, *other_args)

  body_func.__name__ = name
  body: Any = func.FuncOp.from_py_func(*arg_types, name=name)(body_func)
  func_op = cast(func.FuncOp, body.func_op)

  if core_type is not None:
    func_op.attributes["tpu.core_type"] = ir.Attribute.parse(
        f"#tpu.core_type<{core_type}>"
    )

  if dynamic_shape_replacement_enabled:
    # Skip verification for dynamic shape replacement - you can potentially
    # produce ir like ex: add(x[placeholder_0, placeholder_1], y[128, 128])
    # which is not valid, but we don't care since we'll run the verifier again
    # after the dynamic shape replacement pass.
    return body.func_op
  try:
    func_op.verify()
  except ir.MLIRError as e:
    raise error_handling.mlir_error_to_verification_error(e) from e
  return func_op

