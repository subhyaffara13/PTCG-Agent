
def _mpmd_map_lowering(ctx: mlir.LoweringRuleContext, *in_nodes, **params):
  platforms = ctx.module_context.platforms
  if len(platforms) != 1:
    raise NotImplementedError(
        "mpmd_map does not support multi-platform lowering"
    )
  [platform] = platforms
  match platform:
    case "cpu" | "cuda" | "rocm":
      return _mpmd_map_fallback_lowering(ctx, *in_nodes, **params)
    case "tpu":
      return _mpmd_map_tpu_lowering(ctx, *in_nodes, **params)
    case _:
      raise ValueError(f"Unsupported platform: {platform}")

