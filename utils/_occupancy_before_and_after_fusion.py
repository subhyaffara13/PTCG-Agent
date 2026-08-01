
def _occupancy_before_and_after_fusion(
    unfused_n_regs: int,
    fused_n_regs: int,
    fused_n_spills: int,
    num_warps: int,
    device_props: DeviceProperties,
) -> tuple[int, int]:
    if fused_n_spills >= 8:
        return 0, -1

    # # Need device info to calculate occupancy
    regs_per_sm = device_props.regs_per_multiprocessor
    if regs_per_sm is None:
        return 1, 1  # Can't calculate, allow fusion

    assert num_warps
    threads_per_block = num_warps * (device_props.warp_size or 32)

    regs_per_block_unfused = unfused_n_regs * threads_per_block
    regs_per_block_fused = fused_n_regs * threads_per_block

    blocks_unfused = regs_per_sm // regs_per_block_unfused
    blocks_fused = regs_per_sm // regs_per_block_fused

    return blocks_unfused, blocks_fused

