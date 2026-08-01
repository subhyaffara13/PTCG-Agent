
def meta__weight_int8pack_mm(x, w, q_scales):
    torch._check(x.dim() == 2, lambda: "x must be a 2D tensor")
    torch._check(
        x.dtype in [torch.float32, torch.float16, torch.bfloat16],
        lambda: f"expected x to be f32/f16/bf16, got {x.dtype}",
    )
    torch._check(w.dim() == 2, lambda: "w must be a 2D tensor")
    torch._check(
        w.dtype is torch.int8,
        lambda: f"expected w to be int8, got {w.dtype}",
    )
    return x.new_empty(x.size(0), w.size(0), dtype=x.dtype)

