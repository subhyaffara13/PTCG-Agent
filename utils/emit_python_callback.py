from typing import Any

def emit_python_callback(
    ctx: mlir.LoweringRuleContext,
    callback,
    token: Any | None,
    operands: Sequence[ir.Value],
    operand_avals: Sequence[core.ShapedArray],
    result_avals: Sequence[core.ShapedArray],
    *,
    has_side_effect: bool,
    returns_token: bool = True,
    partitioned: bool = False,
    sharding: SdyArrayList | xc.OpSharding | None = None,
) -> tuple[Sequence[mlir.IrValues], Any, Any]:
  """Emits MLIR that calls back to a provided Python function.

  Args:
    ctx: The lowering context.
    callback: The Python callback function.
    token: The token to use for the callback.
    operands: The operands to the callback.
    operand_avals: The abstract values of the operands.
    result_avals: The abstract values of the results.
    has_side_effect: Whether the callback has side effects.
    returns_token: Whether the callback should return a token.
    partitioned: If True, then `callback` is called on local shards only. If
      False, then `callback` is called on all shards.
    sharding: The sharding of the callback.

  Returns:
    A tuple of MLIR result values, a new token (if any), and the host callback
    object.
  """
  if len(ctx.module_context.platforms) > 1:
    raise NotImplementedError("multi-platform lowering for python_callback")
  platform = ctx.module_context.platforms[0]
  if platform not in {"cpu", "cuda", "rocm", "tpu"}:
    raise ValueError(
        f"`EmitPythonCallback` not supported on {platform} backend.")
  if partitioned:
    if platform not in {"cpu", "cuda", "rocm"}:
      raise NotImplementedError(
          f"Partitioned callback not implemented on {platform} backend.")
    if result_avals:
      raise ValueError("Partitioned callback not supported with return values.")
  backend: xc.Client = cast(xc.Client, ctx.module_context.get_backend())
  result_shapes = [_aval_to_xla_shape(aval) for aval in result_avals]
  operand_shapes = [_aval_to_xla_shape(aval) for aval in operand_avals]

  # First we apply checks to ensure output shapes and dtypes match the expected
  # ones.
  def _wrapped_callback(*args):
    out_vals = callback(*args)
    if len(out_vals) != len(result_avals):
      raise RuntimeError(
          "Mismatched number of outputs from callback. "
          "Expected: {}, Actual: {}".format(len(result_avals), len(out_vals)))
    # Handle Python literals, and custom arrays, e.g., tf.Tensor.
    out_vals = tuple(dtypes.canonicalize_value(np.asarray(a)) for a in out_vals)
    for i, (out_val, out_aval) in enumerate(zip(out_vals, result_avals)):
      if out_val.shape != out_aval.shape:
        raise RuntimeError(
            f"Incorrect output shape for return value #{i}: "
            f"Expected: {out_aval.shape}, Actual: {out_val.shape}")
      if out_val.dtype != out_aval.dtype:
        raise RuntimeError(
            f"Incorrect output dtype for return value #{i}: "
            f"Expected: {out_aval.dtype}, Actual: {out_val.dtype}")

    if platform == "tpu":
      # On TPU we cannot receive empty arrays. So, we return from the wrapped
      # callback only the non-empty results, and we will create empty constants
      # in the receiving computation.
      # TODO(b/238239458): fix TPU Recv to work with empty arrays.
      non_empty_out_vals = tuple(
          out_val
          for out_val, result_aval in zip(out_vals, result_avals)
          if not is_empty_shape(result_aval.shape))
      return non_empty_out_vals
    else:
      return out_vals

  if platform == "tpu":
    non_empty_result_avals, non_empty_result_shapes = util.unzip2([
        (aval, shape)
        for aval, shape in zip(result_avals, result_shapes)
        if not is_empty_shape(aval.shape)])
    non_empty_outputs, token = _emit_tpu_python_callback(
        backend, ctx, _wrapped_callback,  token,
        operands, operand_avals, operand_shapes,
        non_empty_result_avals, non_empty_result_shapes,
        returns_token=returns_token, sharding=sharding)
    non_empty_outputs_iter = iter(non_empty_outputs)
    outputs = [
        mlir.ir_constant(np.zeros(result_aval.shape, dtype=result_aval.dtype))
        if is_empty_shape(result_aval.shape) else next(non_empty_outputs_iter)
        for result_aval in result_avals]
    return outputs, token, None

  device = "gpu" if platform in {"cuda", "rocm"} else "cpu"
  partition = "_partitioned" if partitioned else ""
  call_target_name = f"xla_ffi{partition}_python_{device}_callback"
  if token:
    callback_without_token = _wrapped_callback
    def _wrapped_callback(token, *args):
      return (token, *callback_without_token(*args))
    operands = [token, *operands]
    if (
        config.use_shardy_partitioner.value
        and sharding is not None
        and len(ctx.avals_out) > 0
        and isinstance(sharding, SdyArrayList)
    ):
      # Add a sharding annotation for the token if we have at least one
      # output. Otherwise, the single shardy annotation required of all ops
      # (even those without any results) can annotate the token.
      sharding = SdyArrayList((
          SdyArray(mesh_shape=(), dim_shardings=(),
                   logical_device_ids=sharding.shardings[0].logical_device_ids),
          *sharding.shardings))
    ctx = dataclasses.replace(
        ctx,
        avals_in=[core.abstract_token, *ctx.avals_in],
        avals_out=[core.abstract_token, *ctx.avals_out],
    )

  # TODO(dsuo): Remove this line once we deprecate the XLA custom call
  # handler.
  ifrt_callback = _wrapped_callback
  ctx.module_context.add_host_callback(ifrt_callback)
  index = np.uint64(len(ctx.module_context.host_callbacks) - 1)
  result = ffi.build_ffi_lowering_function(
      call_target_name,
      has_side_effect=has_side_effect,
  )(ctx, *operands, index=np.uint64(index))

  if sharding is not None:
    mlir.set_sharding(ctx.module_context, result, sharding)

  results = result.results

  if token:
    token, *results = results

  return results, token, ifrt_callback

