from typing import Any, Callable

def build_ffi_lowering_function(
    call_target_name: str,
    *,
    operand_layouts: Sequence[FfiLayoutOptions] | None = None,
    result_layouts: Sequence[FfiLayoutOptions] | None = None,
    backend_config: Mapping[str, ir.Attribute] | str | None = None,
    skip_ffi_layout_processing: bool = False,
    **lowering_args: Any,
) -> Callable[..., ir.OpView]:
  """Build a lowering op for an foreign function interface (FFI) target.

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

  def _lowering_op(
      ctx: mlir.LoweringRuleContext, *operands: ir.Value, **params: Any
  ) -> ir.OpView:
    kwargs = dict(lowering_args)
    kwargs.setdefault("api_version", 4)
    if kwargs["api_version"] >= 4:
      if backend_config is not None and not isinstance(backend_config, dict):
        raise ValueError(
            "When api_version > 4, backend_config must be a dictionary.")
      kwargs["backend_config"] = dict(
        backend_config or {}, **{k: mlir.ir_attribute(v) for k, v in params.items()})
    else:
      if params:
        raise ValueError(
            "The use of ffi_call attributes requires a custom call API version "
            f"of at least 4; got api_version={kwargs['api_version']}.")
      kwargs["backend_config"] = backend_config
    if "result_types" not in kwargs:
      flat_res_types, _ = mlir.ir_tree_registry.flatten(
          [mlir._aval_to_ir_types(ctx.module_context, a) for a in ctx.avals_out])
      kwargs["result_types"] = flat_res_types
    if not skip_ffi_layout_processing:
      if operand_layouts is None:
        kwargs["operand_layouts"] = map(
            _convert_layout_for_lowering, ctx.avals_in
        )
      else:
        kwargs["operand_layouts"] = [
            _convert_layout_for_lowering(*args)
            for args in zip(ctx.avals_in, operand_layouts)
        ]
      if result_layouts is None:
        kwargs["result_layouts"] = map(
            _convert_layout_for_lowering, ctx.avals_out
        )
      else:
        kwargs["result_layouts"] = [
            _convert_layout_for_lowering(*args)
            for args in zip(ctx.avals_out, result_layouts)
        ]
    if "result_shapes" not in kwargs and not all(
        core.is_constant_shape(_aval_shape(aval)) for aval in ctx.avals_out):
      kwargs["result_shapes"] = [
          mlir.shape_tensor(ctx.module_context, mlir.eval_dynamic_shape_as_ivals(ctx, _aval_shape(aval)))
          for aval in ctx.avals_out]

    return mlir.custom_call(call_target_name, operands=operands, **kwargs)

  return _lowering_op

