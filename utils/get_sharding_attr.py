
def get_sharding_attr(
    ctx: ModuleContext,
    sharding: xc.OpSharding | SdyArray | SdyArrayList
) -> ir.Attribute:
  if isinstance(sharding, (SdyArray, SdyArrayList)):
    return sharding.build(ctx.sharding_attr_cache)
  else:
    # If there are very large numbers of devices, use the proto representation.
    # The MHLO to HLO conversion supports both, and the proto representation is
    # more compact.
    if len(sharding.tile_assignment_devices) > 100:
      return ir.StringAttr.get(sharding.SerializeToString())
    else:
      return ir.StringAttr.get(repr(xc.HloSharding.from_proto(sharding)))

