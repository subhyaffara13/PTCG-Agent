
def addcmul(input, tensor1, tensor2, *, value=1):
    return elementwise_meta(
        input, tensor1, tensor2, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )


def addcmul(self, tensor1, tensor2, *, value=1):
    """
    Computes self + value * tensor1 * tensor2 using FMA for better precision.

    Matches eager CUDA kernel order: self + value * (tensor1 * tensor2)
    This is computed as: fma(value, tensor1 * tensor2, self)

    Note: FMA is only used for floating-point types on non-AMD GPUs. For integer types,
    we fall back to regular arithmetic since FMA doesn't support integers.

    For floating-point types, we use mul_rn (round-to-nearest multiplication)
    to force rounding of the product before the FMA. This prevents Triton's
    compiler from fusing the multiplication with the FMA, matching eager's
    rounding behavior.
    """
    dtype = get_promoted_dtype(
        self,
        tensor1,
        tensor2,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    )

    self_loader = self.make_loader()
    t1_loader = tensor1.make_loader()
    t2_loader = tensor2.make_loader()

    # FMA/mul_rn/div_rn are only available for floating-point types on CUDA (non-AMD)
    device = self.get_device()
    use_fma = (
        dtype.is_floating_point
        and not torch.version.hip
        and device is not None
        and device.type in ["cuda", "xpu"]
    )

    def inner_fn(idx):
        self_val = self_loader(idx)
        t1_val = t1_loader(idx)
        t2_val = t2_loader(idx)

        if value == 1 and use_fma:
            return ops.fma(t1_val, t2_val, self_val)

        # Match eager order: self + value * (tensor1 * tensor2)
        # Compute tensor1 * tensor2 first
        if use_fma:
            # Use mul_rn to force rounding of the product, preventing Triton
            # from fusing t1*t2 with the subsequent FMA
            t1_times_t2 = ops.mul_rn(t1_val, t2_val)
        else:
            t1_times_t2 = ops.mul(t1_val, t2_val)

        # Use index_expr for sympy expressions (e.g., from .item()), constant otherwise
        if isinstance(value, sympy.Basic):
            value_expr = ops.index_expr(value, dtype)
        else:
            value_expr = ops.constant(value, dtype)

        if use_fma:
            # Use FMA for floating-point types for better precision
            return ops.fma(value_expr, t1_times_t2, self_val)
        else:
            # Fall back to regular arithmetic for integer types
            return ops.add(self_val, ops.mul(value_expr, t1_times_t2))

    return Pointwise.create(
        device=self.get_device(),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=self.get_size(),
    )


def addcmul(
    self: TensorLikeType,
    tensor1: TensorLikeType,
    tensor2: TensorLikeType,
    *,
    value: NumberType = 1,
) -> TensorLikeType:
    """
    Reference implementation of torch.addcmul
    """
    if value is not None:
        dtype = self.dtype  # no scalars allowed, see add
        python_type = utils.dtype_to_type(dtype)
        torch._check_value(
            utils.is_weakly_lesser_type(type(value), python_type),
            lambda: f"value argument of type {type(value)} cannot be safely cast to type {python_type}!",
        )

    return self + value * tensor1 * tensor2


def addcmul(g: jit_utils.GraphContext, self, tensor1, tensor2, value=1.0):
    value_tens = g.op("Constant", value_t=torch.tensor([value]))
    return add(g, self, mul(g, mul(g, tensor1, tensor2), value_tens))

