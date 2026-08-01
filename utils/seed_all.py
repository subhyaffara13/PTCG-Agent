
def seed_all() -> None:
    r"""Set the seed for generating random numbers to a random number on all GPUs.

    It's safe to call this function if CUDA is not available; in that
    case, it is silently ignored.
    """

    def cb():
        random_seed = 0
        seeded = False
        for i in range(device_count()):
            default_generator = torch.cuda.default_generators[i]
            if not seeded:
                default_generator.seed()
                random_seed = default_generator.initial_seed()
                seeded = True
            else:
                default_generator.manual_seed(random_seed)

    _lazy_call(cb)


def seed_all() -> int:
    r"""Sets the seed for generating random numbers to a random number on all MTIA devices.

    It's safe to call this function if MTIA is not available; in that case, it is silently ignored.
    """

    def cb():
        random_seed = 0
        seeded = False
        for i in range(device_count()):
            default_generator = default_generators[i]
            if not seeded:
                random_seed = default_generator.seed()
                seeded = True
            else:
                default_generator.manual_seed(random_seed)
        return random_seed

    return _lazy_call(cb, seed_all=True)


def seed_all() -> None:
    r"""Set the seed for generating random numbers to a random number on all GPUs.

    It's safe to call this function if XPU is not available; in that case, it is silently ignored.
    """

    def cb() -> None:
        random_seed = 0
        seeded = False
        for i in range(device_count()):
            default_generator = torch.xpu.default_generators[i]
            if not seeded:
                default_generator.seed()
                random_seed = default_generator.initial_seed()
                seeded = True
            else:
                default_generator.manual_seed(random_seed)

    _lazy_call(cb)

