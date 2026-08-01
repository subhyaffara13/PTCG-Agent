
def addcdiv(input, tensor1, tensor2, *, value=1):
    torch._check(
        not (
            utils.is_integer_dtype(tensor1.dtype)
            and utils.is_integer_dtype(tensor2.dtype)
        ),
        lambda: (
            "Integer division with addcdiv is no longer supported, and in a future ",
            "release addcdiv will perform a true division of tensor1 and tensor2. ",
            "The historic addcdiv behavior can be implemented as ",
            "(input + value * torch.trunc(tensor1 / tensor2)).to(input.dtype) ",
            "for integer inputs and as ",
            "(input + value * tensor1 / tensor2) for float inputs. ",
            "The future addcdiv behavior is just the latter implementation: ",
            "(input + value * tensor1 / tensor2), for all dtypes.",
        ),
    )
    return elementwise_meta(
        input, tensor1, tensor2, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )


def addcdiv(self, tensor1, tensor2, *, value=1):
    """
    Computes self + value * (tensor1 / tensor2) using FMA for better precision.

    Matches eager CUDA kernel order: self + value * (tensor1 / tensor2)
    This is computed as: fma(value, tensor1 / tensor2, self)

    For value=1: self + tensor1 / tensor2 (no FMA needed, just add the division)
    For value!=1: fma(value, div_rn(tensor1, tensor2), self)

    Note: FMA is only used for floating-point types on non-AMD GPUs. For integer types,
    we fall back to regular arithmetic since FMA doesn't support integers.

    We use div_rn (round-to-nearest division) to force proper rounding, preventing
    Triton from fusing operations in ways that change the rounding behavior.
    """
    dtype = get_promoted_dtype(
        self,
        tensor1,
        tensor2,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
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

        # Compute tensor1 / tensor2 first
        # Use div_rn for round-to-nearest division on CUDA to match eager behavior
        if use_fma:
            t1_div_t2 = ops.div_rn(t1_val, t2_val)
        else:
            t1_div_t2 = ops.truediv(t1_val, t2_val)

        if value == 1:
            # For value=1, just add the division result (no FMA needed)
            return ops.add(self_val, t1_div_t2)

        # Use index_expr for sympy expressions (e.g., from .item()), constant otherwise
        if isinstance(value, sympy.Basic):
            value_expr = ops.index_expr(value, dtype)
        else:
            value_expr = ops.constant(value, dtype)

        if use_fma:
            # Use FMA for floating-point types for better precision
            return ops.fma(value_expr, t1_div_t2, self_val)
        else:
            # Fall back to regular arithmetic for integer types
            return ops.add(self_val, ops.mul(value_expr, t1_div_t2))

    return Pointwise.create(
        device=self.get_device(),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=self.get_size(),
    )


def addcdiv(
    self: TensorLikeType,
    tensor1: TensorLikeType,
    tensor2: TensorLikeType,
    *,
    value: NumberType = 1,
) -> TensorLikeType:
    """
    Reference implementation of torch.addcdiv
    """
    if value is not None:
        dtype = self.dtype  # no scalars allowed, see add
        python_type = utils.dtype_to_type(dtype)
        torch._check_value(
            utils.is_weakly_lesser_type(type(value), python_type),
            lambda: f"value argument of type {type(value)} cannot be safely cast to type {python_type}!",
        )

    return self + value * tensor1 / tensor2

