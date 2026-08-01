
def initial_seed() -> int:
    r"""Returns the initial seed for generating random numbers as a
    Python `long`.

    .. note:: The returned seed is for the default generator on CPU only.
    """
    return default_generator.initial_seed()


def initial_seed() -> int:
    r"""Return the current random seed of the current GPU.

    .. warning::
        This function eagerly initializes CUDA.
    """
    _lazy_init()
    idx = current_device()
    default_generator = torch.cuda.default_generators[idx]
    return default_generator.initial_seed()


def initial_seed() -> int:
    r"""Returns the current random seed of the current MTIA device.

    .. warning::
        This function eagerly initializes MTIA.
    """
    _lazy_init()
    idx = current_device()
    return default_generators[idx].initial_seed()


def initial_seed() -> int:
    r"""Return the current random seed of the current GPU.

    .. warning::
        This function eagerly initializes XPU.
    """
    _lazy_init()
    idx = current_device()
    default_generator = torch.xpu.default_generators[idx]
    return default_generator.initial_seed()

