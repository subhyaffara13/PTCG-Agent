
def _fuse_epilogue(
    ms1: float,
    ms2: float,
    unfused_n_regs: int,
    fused_n_regs: int,
    fused_n_spills: int,
    num_warps: int,
    device_props: DeviceProperties,
) -> bool:
    """
    Determine whether to fuse an epilogue into a GEMM template.
    """
    MIN_ACCEPTED_OCCUPANCY = 4
    REGRESSED_OCCUPANCY_RATIO = 0.5

    # Check occupancy impact
    blocks_unfused, blocks_fused = _occupancy_before_and_after_fusion(
        unfused_n_regs, fused_n_regs, fused_n_spills, num_warps, device_props
    )

    epilogue_dominated_with_sufficient_occupancy = ms2 > 2 * ms1 and blocks_fused > 1

    # fuse if no major register spills
    # Occupancy can decrease but if memory bound/epilogue dominated
    # optimistically fuse
    return blocks_fused != -1 and (
        blocks_fused >= MIN_ACCEPTED_OCCUPANCY
        or blocks_fused / blocks_unfused > REGRESSED_OCCUPANCY_RATIO
        or epilogue_dominated_with_sufficient_occupancy
    )

