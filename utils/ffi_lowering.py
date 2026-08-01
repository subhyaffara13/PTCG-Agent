
def ffi_lowering(
    call_target_name: str,
    *,
    operand_layouts: Sequence[FfiLayoutOptions] | None = None,
    result_layouts: Sequence[FfiLayoutOptions] | None = None,
    backend_config: Mapping[str, ir.Attribute] | str | None = None,
    skip_ffi_layout_processing: bool = False,
    **lowering_args: Any
) -> mlir.LoweringRule:
  """Build a lowering rule for an foreign function interface (FFI) target.

  By default, this lowering rule can use the input and output abstract values to
  compute the input and output types and shapes for the custom call, assuming
  row-major layouts.

  Note that layouts passed to this function as tuples should be in
  minor-to-major order (as expected by XLA) rather than major-to-minor as used
  by :func:`~jax.ffi.ffi_call` and ``Layout``.

  If keyword arguments are passed to the lowering rule, these are treated as
  attributes, and added to `backend_config`.

  Args:
    call_target_name: The name of the custom call target.
    operand_layouts: A sequence of layouts (dimension orders) for each operand.
      By default, the operands are assumed to be row-major.
    result_layouts: A sequence of layouts (dimension orders) for each result.
      By default, the results are assumed to be row-major.
    backend_config: Configuration data for the custom call. Any keyword
      arguments passed to the lowering rule will added to this dictionary.
    lowering_args: Any other arguments to :func:`mlir.custom_call` will also be
      passed through if provided as extra arguments to this function.
    skip_ffi_layout_processing: If true, skip processing of operand and result
      layout arguments passed to the lowering rule.
  """

  def _lowering(
    ctx: mlir.LoweringRuleContext, *operands: ir.Value, **params: Any
  ) -> Sequence[ir.Value | Sequence[ir.Value]]:
    result = build_ffi_lowering_function(
        call_target_name,
        operand_layouts=operand_layouts,
        result_layouts=result_layouts,
        backend_config=backend_config,
        skip_ffi_layout_processing=skip_ffi_layout_processing,
        **lowering_args,
    )(ctx, *operands, **params)

    return result.results

  return _lowering

