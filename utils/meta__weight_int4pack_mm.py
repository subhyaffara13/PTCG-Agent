
def meta__weight_int4pack_mm(x, w, q_group_size, q_scale_and_zeros):
    torch._check(x.dim() == 2, lambda: "x must be a 2D tensor")
    expected_dim = 2 if w.fake_device.type == "xpu" else 4
    torch._check(w.dim() == expected_dim, lambda: f"w must be a {expected_dim}D tensor")
    torch._check(
        x.dtype in [torch.float32, torch.float16, torch.bfloat16],
        lambda: f"expected x to be f32/f16/bf16, got {x.dtype}",
    )
    torch._check(
        w.dtype is torch.int32,
        lambda: f"expected w to be int32, got {w.dtype}",
    )
    dim_n = w.size(0) if w.fake_device.type == "xpu" else w.size(0) * 8
    return x.new_empty(x.size(0), dim_n, dtype=x.dtype)

