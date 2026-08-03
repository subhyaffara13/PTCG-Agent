from typing import Any

def ffi_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *operands: ir.Value,
    target_name: str,
    has_side_effect: bool,
    input_layouts: Sequence[Sequence[int]],
    output_layouts: Sequence[Sequence[int]],
    input_output_aliases: Sequence[tuple[int, int]],
    custom_call_api_version: int,
    legacy_backend_config: str | None,
    attributes: Sequence[tuple[str, Any]],
    **_,
) -> Sequence[ir.Value | Sequence[ir.Value]]:
  rule = ffi_lowering(target_name, has_side_effect=has_side_effect,
                      operand_layouts=input_layouts,
                      result_layouts=output_layouts,
                      operand_output_aliases=dict(input_output_aliases),
                      api_version=custom_call_api_version,
                      backend_config=legacy_backend_config)
  return rule(ctx, *operands, **_unwrap_kwargs_hashable(attributes))

