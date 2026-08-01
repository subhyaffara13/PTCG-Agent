
def _buffer_callback_lowering(
    ctx: mlir.LoweringRuleContext,
    *args: Any,
    callback,
    in_tree: Any,
    out_tree: Any,
    has_side_effect: bool,
    input_output_aliases: Sequence[tuple[int, int]],
    command_buffer_compatible: bool,
    **_,
):

  if len(ctx.module_context.platforms) > 1:
    raise NotImplementedError("multi-platform lowering for buffer_callback")
  platform = ctx.module_context.platforms[0]
  target_name = {
      "cpu": "xla_buffer_python_cpu_callback",
      "cuda": "xla_buffer_python_gpu_callback",
      "rocm": "xla_buffer_python_gpu_callback",
  }.get(platform)
  if target_name is None:
    raise ValueError(f"`buffer_callback` not supported on {platform} backend.")

  if command_buffer_compatible and platform in ("cuda", "rocm"):
    target_name += "_cmd_buffer"

  def wrapped_callback(exec_ctx, *args: Any):
    args_in, args_out = util.split_list(args, [in_tree.num_leaves])
    py_args_in, py_kwargs_in = tree_util.tree_unflatten(in_tree, args_in)
    py_args_out = tree_util.tree_unflatten(out_tree, args_out)
    if callback(exec_ctx, py_args_out, *py_args_in, **py_kwargs_in) is not None:
      raise ValueError("buffer_callback callback must not return any values.")
    return ()

  ctx.module_context.add_host_callback(wrapped_callback)
  index = np.uint64(len(ctx.module_context.host_callbacks) - 1)
  rule = ffi.ffi_lowering(
      target_name,
      has_side_effect=has_side_effect,
      operand_output_aliases=dict(input_output_aliases),
  )
  return rule(ctx, *args, index=index)

