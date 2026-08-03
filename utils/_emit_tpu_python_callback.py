from typing import Any

def _emit_tpu_python_callback(
    backend: xc.Client,
    ctx: mlir.LoweringRuleContext,
    callback,
    token: Any | None,
    operands: Sequence[ir.Value],
    operand_avals: Sequence[core.ShapedArray],
    operand_shapes: Sequence[xc.Shape],
    result_avals: Sequence[core.ShapedArray],
    result_shapes: Sequence[xc.Shape],
    *,
    returns_token: bool,
    sharding: SdyArrayList | xc.OpSharding | None = None,
) -> tuple[Sequence[ir.Value], Any]:
  token = token or hlo.create_token()
  _wrapped_callback = callback

  send_channels = []
  if not operand_avals:
    # If there are no operands to the callback, we need to insert a dummy send
    # op or the callback will never be triggered!
    # TODO(sharadmv,chky): Enable this fix in the runtime as opposed to in
    # MLIR builder.
    callback_without_args = _wrapped_callback
    def _wrapped_callback(*args):
      del args
      return callback_without_args()
    send_channel = ctx.module_context.new_channel()
    dummy_send_aval = core.ShapedArray((1,), np.float32)
    dummy_send_val = mlir.ir_constant(np.zeros(1, np.float32))
    operand_shapes = [*operand_shapes, _aval_to_xla_shape(dummy_send_aval)]
    token = send_to_host(ctx.module_context, send_channel, token, dummy_send_val,
                         sharding=sharding)
    send_channels.append(send_channel)
  else:
    for operand in operands:
      channel = ctx.module_context.new_channel()
      token = send_to_host(ctx.module_context, channel, token, operand, sharding=sharding)
      send_channels.append(channel)

  recv_channels = []
  outputs = []
  if returns_token and not result_avals:
    # If the caller expects a token, we need at least one result so that the
    # token from the recv is used as an indication that the callback is
    # complete. Without this, we would only wait for the send to finish.
    callback_without_results = _wrapped_callback
    def _wrapped_callback(*args):
      callback_without_results(*args)
      return 0.0,
    dummy_recv_aval = core.ShapedArray((), np.float32)
    result_shapes = [_aval_to_xla_shape(dummy_recv_aval)]
    channel = ctx.module_context.new_channel()
    token, _ = receive_from_host(
        ctx.module_context, channel, token, dummy_recv_aval, sharding=sharding
    )
    recv_channels.append(channel)
  else:
    for result_aval in result_avals:
      channel = ctx.module_context.new_channel()
      assert isinstance(result_aval, core.ShapedArray)
      token, out = receive_from_host(
          ctx.module_context, channel, token, result_aval, sharding=sharding
      )
      outputs.append(out)
      recv_channels.append(channel)
  ifrt_callback = backend.make_python_callback_from_host_send_and_recv(
      _wrapped_callback, operand_shapes, result_shapes, send_channels,
      recv_channels, pickle_util.dumps)
  ctx.module_context.add_host_callback(ifrt_callback)
  return outputs, token

