
def register_lowering_rule(params_cls, rule, platform: str):
  _backend_lowering_rules[params_cls] = (rule, platform)


def register_lowering_rule(
    prim: jax_core.Primitive,
    *,
    kernel_types: Collection[tpu_core.CoreType] = (tpu_core.CoreType.TC,),
    ensure_mlir_values: bool = True,
) -> Callable[[T], T]:
  def decorator(rule: T) -> T:
    for kernel_type in kernel_types:
      lowering_rules[kernel_type][prim] = rule
      if not ensure_mlir_values:
        skip_mlir_conversions.add((prim, kernel_type))
    return rule

  return decorator


def register_lowering_rule(
    primitive: jax_core.Primitive,
    lowering_semantics: mgpu.LoweringSemantics,
    primitive_semantics: gpu_core.PrimitiveSemantics = gpu_core.PrimitiveSemantics.Warpgroup,
):
  def deco(fn):
    mosaic_lowering_rules[
        (lowering_semantics, primitive_semantics)][primitive] = fn
    return fn

  return deco

