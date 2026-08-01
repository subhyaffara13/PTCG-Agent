
def receive_from_host(
    ctx: mlir.ModuleContext,
    channel: int,
    token: ir.Value[hlo.TokenType],
    out_aval: core.ShapedArray,
    name: str | None = None,
    *,
    sharding: SdyArrayList | xc.OpSharding | None = None,
) -> tuple[ir.Value, ir.Value]:
  channel_handle = hlo.ChannelHandle.get(channel, mlir.RECV_FROM_HOST_TYPE)
  out_type = mlir.aval_to_ir_type(ctx, out_aval)
  recv_op = hlo.RecvOp([out_type,
                        hlo.TokenType.get()], token, channel_handle,
                        is_host_transfer=ir.BoolAttr.get(True))
  recv_op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(
      dict(
          _xla_host_transfer_handler_name=ir.StringAttr.get(
              _XLA_HOST_TRANSFER_PJRT_RENDEZVOUS_HANDLER_NAME
          ),
          _xla_host_transfer_rendezvous=ir.StringAttr.get(str(channel)),
      )
  )
  if sharding is not None:
    if config.use_shardy_partitioner.value:
      assert isinstance(sharding, SdyArrayList)
      assert len(sharding.shardings) >= 1
      # `RecvOp`'s last argument is a `TokenType`. Since Shardy requires the
      # number of shardings to match the number of results, but JAX only sees
      # the array result, we need to add an equivalent sharding for the token.
      # Note that even if a function returns N results, we will end up with N
      # `RecvOp`s, so we only need to get the first sharding. All shardings are
      # the same anyways, operating on the same single device ID.
      sharding = SdyArrayList((
          sharding.shardings[0],
          SdyArray(mesh_shape=(), dim_shardings=(),
                   logical_device_ids=sharding.shardings[0].logical_device_ids)))
    mlir.set_sharding(ctx, recv_op, sharding)
  # Token should be at the end of the results
  result, token = recv_op.results
  return token, result

