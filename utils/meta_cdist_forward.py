
def meta_cdist_forward(x1, x2, p, compute_mode):
    torch._check(
        x1.dim() >= 2,
        lambda: f"cdist only supports at least 2D tensors, X1 got: {x1.dim()}D",
    )
    torch._check(
        x2.dim() >= 2,
        lambda: f"cdist only supports at least 2D tensors, X2 got: {x2.dim()}D",
    )
    torch._check(
        x1.size(-1) == x2.size(-1),
        lambda: f"X1 and X2 must have the same number of columns. X1: {x1.size(-1)} X2: {x2.size(-1)}",
    )
    torch._check(
        utils.is_float_dtype(x1.dtype),
        lambda: f"cdist only supports floating-point dtypes, X1 got: {x1.dtype}",
    )
    torch._check(
        utils.is_float_dtype(x2.dtype),
        lambda: f"cdist only supports floating-point dtypes, X2 got: {x2.dtype}",
    )
    torch._check(p >= 0, lambda: "cdist only supports non-negative p values")
    torch._check(
        compute_mode in (None, 0, 1, 2),
        lambda: f"possible modes: None, 0, 1, 2, but was: {compute_mode}",
    )
    r1 = x1.size(-2)
    r2 = x2.size(-2)
    batch_tensor1 = x1.shape[:-2]
    batch_tensor2 = x2.shape[:-2]
    output_shape = list(torch.broadcast_shapes(batch_tensor1, batch_tensor2))
    output_shape.extend([r1, r2])
    return x1.new_empty(output_shape)

