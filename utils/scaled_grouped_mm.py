
def scaled_grouped_mm(
    mat_a: Tensor,
    mat_b: Tensor,
    scale_a: Tensor | list[Tensor],
    scale_recipe_a: ScalingType | list[ScalingType],
    scale_b: Tensor | list[Tensor],
    scale_recipe_b: ScalingType | list[ScalingType],
    swizzle_a: SwizzleType | list[SwizzleType] | None = None,
    swizzle_b: SwizzleType | list[SwizzleType] | None = None,
    bias: Tensor | None = None,
    offs: Tensor | None = None,
    output_dtype: torch.dtype | None = torch.bfloat16,
    contraction_dim: list[int] | tuple[int, ...] = (),
    use_fast_accum: bool = False,
) -> Tensor:
    r"""
    scaled_grouped_mm(mat_a, mat_b, scale_a, scale_recipe_a, scale_b, scale_recipe_b, swizzle_a, swizzle_b, bias, offs,
              output_dtype, use_fast_accum)

    Applies a grouped scaled matrix-multiply, grouped_mm(mat_a, mat_b) where the scaling of mat_a and mat_b are described by
    scale_recipe_a and scale_recipe_b respectively.

    Args:
        scale_a: Tensor containing decoding scaling factors for mat_a
        scale_recipe_a: Enum describing how mat_a has been scaled
        scale_b: Tensor containing decoding scaling factors for mat_b
        scale_recipe_b: Enum describing how mat_b has been scaled
        swizzle_a: Enum describing the swizzling pattern (if any) of scale_a
        swizzle_b: Enum describing the swizzling pattern (if any) of scale_b
        bias: optional bias term to be added to the output
        offs: optional offsets into the source tensors denoting group start indices
        output_dtype: dtype used for the output tensor
        contraction_dim: describe which dimensions are :math:`K` in the matmul.
        use_fast_accum: enable/disable tensor-core fast accumulation (Hopper-GPUs only)
    """

    def expand_single_value(v: _Any | list[_Any] | None) -> list[_Any]:
        if v is None:
            return []
        elif not isinstance(v, (list)):
            return [
                v,
            ]
        else:
            return v

    scale_a = expand_single_value(scale_a)
    scale_recipe_a = expand_single_value(scale_recipe_a)
    scale_b = expand_single_value(scale_b)
    scale_recipe_b = expand_single_value(scale_recipe_b)
    swizzle_a = expand_single_value(swizzle_a)
    swizzle_b = expand_single_value(swizzle_b)

    # native_functions has restrictions on what can be defined
    # & passed through - std::optional<ArrayRef<Tensor>> for instance
    # *cannot* be passed, but an empty vector (list) can.
    # So, we need to convert None arguments for lists in python
    # explicitly into empty lists.
    def list_or_empty(l: list[_Any] | None) -> list[_Any]:
        return l if l else []

    def enum_list_as_int_list(l: _Any | list[_Any]) -> list[_Any]:
        if not isinstance(l, list):
            l = [
                l,
            ]
        return [li.value for li in l]

    out = torch._scaled_grouped_mm_v2(
        mat_a,
        mat_b,
        scale_a,
        enum_list_as_int_list(scale_recipe_a),
        enum_list_as_int_list(list_or_empty(swizzle_a)),
        scale_b,
        enum_list_as_int_list(scale_recipe_b),
        enum_list_as_int_list(list_or_empty(swizzle_b)),
        offs,
        bias,
        output_dtype,
        contraction_dim,
        use_fast_accum,
    )

    return out

