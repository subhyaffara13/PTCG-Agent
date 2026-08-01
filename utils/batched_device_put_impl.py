
def batched_device_put_impl(
    *xs,
    devices: Sequence[Device | Sharding | Format | None],
    srcs: Sequence[Device | Sharding | Format | None],
    copy_semantics: Sequence[ArrayCopySemantics]):
  return _batched_device_put_impl(
      *xs, devices=devices, srcs=srcs, copy_semantics=copy_semantics,
      dst_avals=[None] * len(devices))

