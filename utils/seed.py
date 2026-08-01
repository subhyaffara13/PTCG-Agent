
def seed() -> int:
    r"""Sets the seed for generating random numbers to a non-deterministic
    random number on all devices. Returns a 64 bit number used to seed the RNG.
    """
    seed = default_generator.seed()
    import torch.cuda

    if not torch.cuda._is_in_bad_fork():
        torch.cuda.manual_seed_all(seed)

    import torch.mps

    if not torch.mps._is_in_bad_fork():
        torch.mps.manual_seed(seed)

    import torch.xpu

    if not torch.xpu._is_in_bad_fork():
        torch.xpu.manual_seed_all(seed)

    import torch.mtia

    if not torch.mtia._is_in_bad_fork():
        torch.mtia.manual_seed_all(seed)

    _seed_custom_device(seed)

    return seed


def seed() -> None:
    r"""Set the seed for generating random numbers to a random number for the current GPU.

    It's safe to call this function if CUDA is not available; in that
    case, it is silently ignored.

    .. warning::
        If you are working with a multi-GPU model, this function will only initialize
        the seed on one GPU.  To initialize all GPUs, use :func:`seed_all`.
    """

    def cb():
        idx = current_device()
        default_generator = torch.cuda.default_generators[idx]
        default_generator.seed()

    _lazy_call(cb)


def seed() -> None:
    r"""Sets the seed for generating random numbers to a random number."""
    _get_default_mps_generator().seed()


def seed() -> int:
    r"""Sets the seed for generating random numbers to a random number for the current MTIA device.
    It's safe to call this function if MTIA is not available; in that case, it is silently ignored.

    .. warning::
        If you are working with a multi-GPU model, this function will only initialize
        the seed on one GPU.  To initialize all GPUs, use :func:`seed_all`.
    """

    def cb():
        idx = current_device()
        default_generator = default_generators[idx]
        return default_generator.seed()

    return _lazy_call(cb, seed=True)


def seed() -> None:
    r"""Set the seed for generating random numbers to a random number for the current GPU.

    It's safe to call this function if XPU is not available; in that case, it is silently ignored.

    .. warning::
        If you are working with a multi-GPU model, this function will only initialize
        the seed on one GPU.  To initialize all GPUs, use :func:`seed_all`.
    """

    def cb() -> None:
        idx = current_device()
        default_generator = torch.xpu.default_generators[idx]
        default_generator.seed()

    _lazy_call(cb)


def seed(seed=None):
    if seed is not None:
        torch.random.manual_seed(seed)


def seed(a=None, version=2):
    rng.seed(a=a, version=version)
    _assumptions_rng.seed(a=a, version=version)

