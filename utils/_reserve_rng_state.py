
def _reserve_rng_state(device: torch.device, used_offset):
    """
    Reserve `used_offset` 32-bit Philox samples on the given CUDA device and
    return (seed, base), where base is in Philox-4x32 units.

    This mirrors how Inductor accounts for Philox consumption so compiled
    dropout kernels can reconstruct eager RNG state.
    """
    dev = device if isinstance(device, torch.device) else torch.device(device)
    if dev.type != "cuda":
        # Only CUDA devices have Philox-based CUDAGenerator. For non-CUDA
        # devices this prim should be dead code and never actually run.
        return 0, 0

    dev_index = _get_device_index(dev, optional=True)
    if dev_index is None:
        dev_index = torch.cuda.current_device()

    gen = torch.cuda.default_generators[dev_index]
    seed_t, off_t, intra_t = torch.ops.inductor_prims.inductor_reserve_rng_state(
        gen, used_offset
    )

    # NOTE: for correctness in eager, intra_t should be 0.
    # Keep everything as tensor math to avoid host sync.
    if intra_t.device.type != off_t.device.type:
        intra = int(intra_t.item())
        base = torch.div(off_t + intra, 4, rounding_mode="floor")
    else:
        base = torch.div(off_t + intra_t, 4, rounding_mode="floor")
    return seed_t, base

