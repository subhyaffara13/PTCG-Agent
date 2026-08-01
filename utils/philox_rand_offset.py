
def philox_rand_offset(shape):
    """
    TorchInductor offset calculation differs from PyTorch eager offset
    calculation for random ops (tl.rand vs torch.rand). In future, we should
    strive for same impl for tl.rand and torch.rand.
    """
    numel = 1
    for s in shape:
        numel = numel * s
    return tensor(numel, dtype=torch.int64)


def philox_rand_offset(
    shape: torch.Size,
):
    # For impl, look at the function calc_execution_policy in the file
    # aten/src/ATen/native/cuda/DistributionTemplates.h. The impl was copied at
    # commit hash 72aa0667bd16707d50eb8fa337092a1f5d11dfb6
    numel_scalar = 1
    for dim_size in shape:
        numel_scalar *= dim_size
    numel = torch.scalar_tensor(numel_scalar, dtype=torch.int64)

    block_size = 256
    unroll = 4
    curand4_engine_calls = 4
    device_property = torch.cuda.get_device_properties(torch.cuda.current_device())
    blocks_per_sm = device_property.max_threads_per_multi_processor // block_size
    num = cast(int, numel)
    grid_size = (num + block_size - 1) // block_size
    grid_size = min(grid_size, device_property.multi_processor_count * blocks_per_sm)
    return ((num - 1) // (block_size * grid_size * unroll) + 1) * curand4_engine_calls

