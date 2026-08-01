
def adapt_config_for_tiling(
    size_hints,
    tiling_scores,
    original_x,
    original_r,
    num_warps=None,
    num_stages=1,
    register_intensive=False,
    persistent_reduction=False,
    waves_per_eu=None,
) -> Config:
    """
    Create an adapted configuration based on tiling scores,
    redistributing the same total block size (x * r) according to tiling scores.
    """
    assert all(s in tiling_scores for s in size_hints)
    target_block_product = original_x * original_r
    block_sizes = match_target_block_product(
        size_hints, tiling_scores, target_block_product
    )

    return triton_config_tiled_reduction(
        size_hints,
        block_sizes["x"],
        block_sizes["y"],
        block_sizes["r0_"],
        num_stages=num_stages,
        register_intensive=register_intensive,
        waves_per_eu=waves_per_eu,
    )

