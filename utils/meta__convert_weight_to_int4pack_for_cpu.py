
def meta__convert_weight_to_int4pack_for_cpu(w, inner_k_tiles):
    torch._check(w.dim() == 2, lambda: "w must be a 2D tensor")
    torch._check(
        w.dtype is torch.int32,
        lambda: f"expected w to be int32, got {w.dtype}",
    )
    n = w.size(0)
    k = w.size(1)  # w is [n][k] int32
    return w.new_empty(
        (n, k // 2),
        dtype=torch.uint8,
    )

