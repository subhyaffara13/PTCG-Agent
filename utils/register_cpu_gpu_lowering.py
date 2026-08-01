
def register_cpu_gpu_lowering(
    prim, lowering_rule, supported_platforms=("cpu", "cuda", "rocm")
):
  for platform in supported_platforms:
    prefix = _platform_prefix_map[platform]
    mlir.register_lowering(
        prim,
        partial(lowering_rule, target_name_prefix=prefix),
        platform=platform)

