
def add_nv_universal_gemm_choices(
    choices: list[ChoiceCaller],
    layout: Layout,
    inputs: MMKernelInputs,
    accumulator_type: torch.dtype | None = None,
) -> None:
    """
    Add NVIDIA Universal GEMM kernels to the autotune choices.

    Thin wrapper around _add_nv_gemm_choices_impl for regular GEMM.
    """
    if not ensure_nv_universal_gemm_available():
        log.debug("cutlass_api not available, skipping NVIDIA Universal GEMM choices")
        return

    _add_nv_gemm_choices_impl(
        choices=choices,
        layout=layout,
        input_nodes=inputs.nodes(),
        variant=GemmVariant.GEMM,
        accumulator_type=accumulator_type or torch.float32,
        mm_inputs=inputs,
    )

