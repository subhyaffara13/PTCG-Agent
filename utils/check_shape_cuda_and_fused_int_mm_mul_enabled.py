
def check_shape_cuda_and_fused_int_mm_mul_enabled(match):
    return (
        config.force_fuse_int_mm_with_mul
        and len(getattr(match.args[2].meta.get("val"), "shape", [])) == 2
        and getattr(match.args[2].meta.get("val"), "is_cuda", False)
    )

