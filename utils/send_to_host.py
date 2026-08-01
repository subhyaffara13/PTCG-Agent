
def send_to_host(
    ctx: mlir.ModuleContext,
    channel: int,
    token: ir.Value[hlo.TokenType],
    operand: Any,
    name: str | None = None,
    *,
    sharding: SdyArrayList | xc.OpSharding | None = None,
) -> ir.Value:
  channel_handle = hlo.ChannelHandle.get(channel, mlir.SEND_TO_HOST_TYPE)
  send_op = hlo.SendOp([operand], token, channel_handle,
                        is_host_transfer=ir.BoolAttr.get(True))
  send_op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(
      dict(
          _xla_host_transfer_handler_name=ir.StringAttr.get(
              _XLA_HOST_TRANSFER_PJRT_RENDEZVOUS_HANDLER_NAME
          ),
          _xla_host_transfer_rendezvous=ir.StringAttr.get(str(channel)),
      )
  )
  if sharding is not None:
    if config.use_shardy_partitioner.value:
      # `SendOp`'s return type is a StableHLO `TokenType`. However JAX passed
      # in the maximal sharding of the array type. Since a token has no rank,
      # we need to create an equivalent sharding with no dimensions. If there
      # are multiple shardings, just grab the first one since all these
      # shardings should be the same.
      assert isinstance(sharding, SdyArrayList)
      assert len(sharding.shardings) >= 1
      sharding = SdyArrayList((SdyArray(
          mesh_shape=(), dim_shardings=(),
          logical_device_ids=sharding.shardings[0].logical_device_ids),))
    mlir.set_sharding(ctx, send_op, sharding)
  return send_op.result

