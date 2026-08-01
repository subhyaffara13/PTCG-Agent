
def set_sharding(ctx: ModuleContext, op,
                 sharding: xc.OpSharding | SdyArray | SdyArrayList):
  if isinstance(sharding, (SdyArray, SdyArrayList)):
    op.attributes["sdy.sharding"] = get_sharding_attr(ctx, sharding)
  else:
    op.attributes["mhlo.sharding"] = get_sharding_attr(ctx, sharding)

