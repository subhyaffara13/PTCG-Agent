
def _shape_to_offset(shape, device: torch.device):
    # Modified from torch/_prims/rng_prims.py:philox_rand_offset
    nelem = 1
    for s in shape:
        nelem *= s

    # Empty tensor: no random numbers are generated/consumed.
    is_empty = nelem == 0
    if statically_known_true(is_empty) or guard_or_false(is_empty):
        return 0

    if device is None:
        device = torch.device("cpu")
    elif isinstance(device, str):
        device = torch.device(device)

    if device.type != "cuda":
        return 0

    block_size = 256
    unroll = 4
    curand4_engine_calls = 4

    device_property = torch.cuda.get_device_properties(device)

    blocks_per_sm = device_property.max_threads_per_multi_processor // block_size
    max_grid = device_property.multi_processor_count * blocks_per_sm
    grid_size = (nelem + block_size - 1) // block_size
    grid_size = -torch.sym_min(-grid_size, -1)
    grid_size = torch.sym_min(grid_size, max_grid)

    return ((nelem - 1) // (block_size * grid_size * unroll) + 1) * curand4_engine_calls

