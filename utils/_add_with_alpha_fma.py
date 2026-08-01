
def _add_with_alpha_fma(a, b, alpha):
    """Compute a + alpha * b using FMA for CUDA floating-point precision."""
    dtype = get_promoted_dtype(
        a,
        b,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    )
    a_loader = a.make_loader()
    b_loader = b.make_loader()

    def inner_fn(idx):
        a_val = a_loader(idx)
        b_val = b_loader(idx)
        if isinstance(alpha, sympy.Basic):
            alpha_expr = ops.index_expr(alpha, dtype)
        else:
            alpha_expr = ops.constant(alpha, dtype)
        return ops.fma(b_val, alpha_expr, a_val)

    return Pointwise.create(
        device=a.get_device(),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=a.get_size(),
    )

