
def _batched_device_put_impl(
    *xs,
    devices: Sequence[Device | Sharding | Format | None],
    srcs: Sequence[Device | Sharding | Format | None],
    copy_semantics: Sequence[ArrayCopySemantics],
    dst_avals: Sequence[core.ShapedArray | None]):
  ys = []
  dsa_indices, dsa_xs, dsa_shardings, dsa_copy_semantics = [], [], [], []
  dca_indices, dca_xs, dca_shardings, dca_device_lists, dca_copy_semantics = \
    [], [], [], [], []

  for i, (x, device, src, cp, aval) in enumerate(
      zip(xs, devices, srcs, copy_semantics, dst_avals)):
    y = _device_put_impl(x, device=device, src=src, copy=cp, aval=aval)
    if isinstance(y, _DeferredShardArg):
      dsa_indices.append(i)
      dsa_xs.append(y.x)
      dsa_shardings.append(y.s)
      dsa_copy_semantics.append(y.copy_semantics)
    elif isinstance(y, _DeferredCrossHostTransferArg):
      dca_indices.append(i)
      dca_xs.append(y.x)
      dca_shardings.append(y.dst_sharding)
      dca_device_lists.append(y.dst_sharding._internal_device_list)
      dca_copy_semantics.append(y.copy_semantics)
    ys.append(y)

  if dsa_xs:
    shard_arg_results = pxla.shard_args(dsa_shardings, [None] * len(dsa_xs),
                                        dsa_copy_semantics, dsa_xs)
    for i, shard_arg_result in zip(dsa_indices, shard_arg_results):
      assert isinstance(ys[i], _DeferredShardArg)
      ys[i] = ys[i].result_handler(shard_arg_result)
  if dca_xs:
    copy_array_results = xc.batched_copy_array_to_devices_with_sharding(
      dca_xs, dca_device_lists, dca_shardings, dca_copy_semantics)
    for i, copy_array_result in zip(dca_indices, copy_array_results):
      assert isinstance(ys[i], _DeferredCrossHostTransferArg)
      ys[i] = copy_array_result

  return ys

