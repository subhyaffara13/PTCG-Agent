
def commit_arrive(
    barrier: utils.BarrierRef | ir.Value,
    collective: bool = False,
    ctx: LaunchContext | None = None,
) -> None:
  if isinstance(barrier, utils.BarrierRef):
    barrier = barrier.get_ptr()
  elif barrier.type != llvm.PointerType.get(address_space=3):
    raise ValueError(
        "barrier must be a Mosaic barrier or a SMEM pointer, got:"
        f" {barrier.type}"
    )
  if collective:
    if ctx is None:
      raise ValueError("ctx must be provided for collective barriers")
    # TODO(apaszke): This is just 0b11 shifted by the even CTA index.
    if ctx.cluster_size != (2, 1, 1):
      raise NotImplementedError("Collective arrivals only support (2, 1, 1)-shaped clusters")
    i16 = ir.IntegerType.get_signless(16)
    mask = arith.constant(i16, 3)
    nvvm.tcgen05_commit(
        barrier, group=nvvm.CTAGroupKind.CTA_2, multicast_mask=mask
    )
  else:
    nvvm.tcgen05_commit(barrier)

