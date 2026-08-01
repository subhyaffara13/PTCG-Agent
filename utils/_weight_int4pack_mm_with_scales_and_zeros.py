
def _weight_int4pack_mm_with_scales_and_zeros(x, w, q_group_size, qScale, qZeros):
    torch._check(x.dim() == 2, lambda: "x must be a 2D tensor")
    torch._check(w.dim() == 2, lambda: "w must be a 2D tensor")
    torch._check(
        x.dtype in [torch.float32, torch.float16, torch.bfloat16],
        lambda: f"expected x to be f32/f16/bf16, got {x.dtype}",
    )
    torch._check(
        w.dtype is torch.int32,
        lambda: f"expected w to be int32, got {w.dtype}",
    )
    return x.new_empty(x.size(0), w.size(0), dtype=x.dtype)

