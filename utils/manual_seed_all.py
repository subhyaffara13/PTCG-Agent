
def manual_seed_all(seed: int) -> None:
    r"""Set the seed for generating random numbers on all GPUs.

    It's safe to call this function if CUDA is not available; in that
    case, it is silently ignored.

    Args:
        seed (int): The desired seed.
    """
    seed = int(seed)

    def cb():
        for i in range(device_count()):
            default_generator = torch.cuda.default_generators[i]
            default_generator.manual_seed(seed)

    _lazy_call(cb, seed_all=True)


def manual_seed_all(seed: int) -> None:
    r"""Sets the seed for generating random numbers on all MTIA devices.
    It's safe to call this function if MTIA is not available; in that case, it is silently ignored.

    Args:
        seed (int): The desired seed.
    """
    seed = int(seed)

    def cb():
        for i in range(device_count()):
            default_generator = default_generators[i]
            default_generator.manual_seed(seed)

    _lazy_call(cb, seed_all=True)


def manual_seed_all(seed: int) -> None:
    r"""Set the seed for generating random numbers on all GPUs.

    It's safe to call this function if XPU is not available; in that case, it is silently ignored.

    Args:
        seed (int): The desired seed.
    """
    seed = int(seed)

    def cb() -> None:
        for i in range(device_count()):
            default_generator = torch.xpu.default_generators[i]
            default_generator.manual_seed(seed)

    _lazy_call(cb, seed_all=True)

