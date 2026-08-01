
def meta__convert_weight_to_int4pack(w, inner_k_tiles):
    torch._check(w.dim() == 2, lambda: "w must be a 2D tensor")
    torch._check(
        w.dtype is torch.uint8,
        lambda: f"expected w to be uint8, got {w.dtype}",
    )
    n = w.size(0)
    k = w.size(1) * 2  # w is [n][k / 2] uint8
    return w.new_empty(
        (
            n // 8,
            k // (inner_k_tiles * 16),
            32,
            inner_k_tiles // 2,
        ),
        dtype=torch.int32,
    )

