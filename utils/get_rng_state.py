
def get_rng_state() -> torch.Tensor:
    r"""Returns the random number generator state as a `torch.ByteTensor`.

    .. note:: The returned state is for the default generator on CPU only.

    See also: :func:`torch.random.fork_rng`.
    """
    return default_generator.get_state()


def get_rng_state(device: int | str | torch.device = "cuda") -> Tensor:
    r"""Return the random number generator state of the specified GPU as a ByteTensor.

    Args:
        device (torch.device or int, optional): The device to return the RNG state of.
            Default: ``'cuda'`` (i.e., ``torch.device('cuda')``, the current CUDA device).

    .. warning::
        This function eagerly initializes CUDA.
    """
    _lazy_init()
    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("cuda", device)
    idx = device.index
    if idx is None:
        idx = current_device()
    default_generator = torch.cuda.default_generators[idx]
    return default_generator.get_state()


def get_rng_state(device: int | str | torch.device = "mps") -> Tensor:
    r"""Returns the random number generator state as a ByteTensor.

    Args:
        device (torch.device or int, optional): The device to return the RNG state of.
            Default: ``'mps'`` (i.e., ``torch.device('mps')``, the current MPS device).
    """
    return _get_default_mps_generator().get_state()


def get_rng_state(device: Device = "mtia") -> Tensor:
    r"""Returns the random number generator state of the specified MTIA device as a ByteTensor.

    Args:
        device (torch.device or int, optional): The device to return the RNG state of.
            Default: ``'mtia'`` (i.e., ``torch.device('mtia')``, the current mtia device).

    .. warning::
        This function eagerly initializes MTIA.
    """
    _lazy_init()
    idx = _get_device_index(device, optional=True)
    if idx is None:
        idx = current_device()
    default_generator = default_generators[idx]
    return default_generator.get_state()


def get_rng_state(device: int | str | torch.device = "xpu") -> Tensor:
    r"""Return the random number generator state of the specified GPU as a ByteTensor.

    Args:
        device (torch.device or int, optional): The device to return the RNG state of.
            Default: ``'xpu'`` (i.e., ``torch.device('xpu')``, the current XPU device).

    .. warning::
        This function eagerly initializes XPU.
    """
    _lazy_init()
    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("xpu", device)
    idx = device.index
    if idx is None:
        idx = current_device()
    default_generator = torch.xpu.default_generators[idx]
    return default_generator.get_state()

