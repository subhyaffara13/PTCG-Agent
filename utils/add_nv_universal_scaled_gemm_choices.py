
def add_nv_universal_scaled_gemm_choices(
    choices: list[ChoiceCaller],
    layout: Layout,
    input_nodes: list[Buffer],
    accumulator_type: torch.dtype | None = None,
    kernel_inputs: MMKernelInputs | None = None,
) -> None:
    """
    Add NVIDIA Universal Scaled GEMM (FP8) kernels to the autotune choices.

    The scaling type is inferred from the input shapes/dtypes.
    If the scaling mode is unsupported by NVGEMM, this function returns without
    adding any choices.
    """
    if not ensure_nv_universal_gemm_available():
        return

    from torch._inductor.utils import infer_scale_swizzle_ir

    if len(input_nodes) < 4:
        return

    mat_a, mat_b, scale_a, scale_b = input_nodes[:4]

    scale_type_a, swizzle_type_a = infer_scale_swizzle_ir(mat_a, scale_a)
    scale_type_b, swizzle_type_b = infer_scale_swizzle_ir(
        mat_b, scale_b, transpose=True
    )

    if scale_type_a is None or scale_type_b is None:
        return

    _add_nv_gemm_choices_impl(
        choices=choices,
        layout=layout,
        input_nodes=input_nodes,
        variant=GemmVariant.SCALED_GEMM,
        accumulator_type=accumulator_type or torch.float32,
        mm_inputs=kernel_inputs,
        scale_type_a=scale_type_a,
        scale_type_b=scale_type_b,
        swizzle_type_a=swizzle_type_a,
        swizzle_type_b=swizzle_type_b,
    )

