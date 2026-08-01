
def add_nv_universal_grouped_gemm_choices(
    choices: list[ChoiceCaller],
    layout: Layout,
    input_nodes: list[Buffer],
    accumulator_type: torch.dtype | None = None,
) -> None:
    """
    Add NVIDIA Universal Grouped GEMM kernels to the autotune choices.

    Thin wrapper around _add_nv_gemm_choices_impl for grouped GEMM.

    For grouped GEMM (contiguous offset variant):
    - A is (TotalM, K) with problems stacked along M
    - B is (G, K, N) where B[i] is the weight for problem i
    - offsets is (G,) marking where each problem ends in A
    - Output is (TotalM, N)
    """
    if not ensure_nv_universal_gemm_available():
        log.debug(
            "cutlass_api not available, skipping NVIDIA Universal Grouped GEMM choices"
        )
        return

    _add_nv_gemm_choices_impl(
        choices=choices,
        layout=layout,
        input_nodes=input_nodes,
        variant=GemmVariant.GROUPED_GEMM,
        accumulator_type=accumulator_type or torch.float32,
    )

