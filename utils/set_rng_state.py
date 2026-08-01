
def set_rng_state(new_state: torch.Tensor) -> None:
    r"""Sets the random number generator state.

    .. note:: This function only works for CPU. For CUDA, please use
        :func:`torch.manual_seed`, which works for both CPU and CUDA.

    Args:
        new_state (torch.ByteTensor): The desired state
    """
    default_generator.set_state(new_state)


def set_rng_state(new_state: Tensor, device: int | str | torch.device = "cuda") -> None:
    r"""Set the random number generator state of the specified GPU.

    Args:
        new_state (torch.ByteTensor): The desired state
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``'cuda'`` (i.e., ``torch.device('cuda')``, the current CUDA device).
    """
    if not is_initialized():
        with torch._C._DisableFuncTorch():
            # Clone the state because the callback will be triggered
            # later when CUDA is lazy initialized.
            new_state = new_state.clone(memory_format=torch.contiguous_format)
    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("cuda", device)

    def cb():
        idx = device.index
        if idx is None:
            idx = current_device()
        default_generator = torch.cuda.default_generators[idx]
        default_generator.set_state(new_state)

    _lazy_call(cb)


def set_rng_state(new_state: Tensor, device: int | str | torch.device = "mps") -> None:
    r"""Sets the random number generator state.

    Args:
        new_state (torch.ByteTensor): The desired state
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``'mps'`` (i.e., ``torch.device('mps')``, the current MPS device).
    """
    new_state_copy = new_state.clone(memory_format=torch.contiguous_format)
    _get_default_mps_generator().set_state(new_state_copy)


def set_rng_state(new_state: Tensor, device: Device = "mtia") -> None:
    r"""Sets the random number generator state of the specified MTIA device.

    Args:
        new_state (torch.ByteTensor): The desired state
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``'mtia'`` (i.e., ``torch.device('mtia')``, the current mtia device).
    """
    if not is_initialized():
        with torch._C._DisableFuncTorch():
            # Clone the state because the callback will be triggered
            # later when MTIA is lazy initialized.
            new_state = new_state.clone(memory_format=torch.contiguous_format)

    idx = _get_device_index(device, optional=True)
    if idx is None:
        idx = current_device()

    def cb():
        default_generator = default_generators[idx]
        default_generator.set_state(new_state)

    _lazy_call(cb)


def set_rng_state(new_state: Tensor, device: int | str | torch.device = "xpu") -> None:
    r"""Set the random number generator state of the specified GPU.

    Args:
        new_state (torch.ByteTensor): The desired state
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``'xpu'`` (i.e., ``torch.device('xpu')``, the current XPU device).
    """
    if not is_initialized():
        with torch._C._DisableFuncTorch():
            new_state = new_state.clone(memory_format=torch.contiguous_format)

    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("xpu", device)

    def cb() -> None:
        idx = device.index
        if idx is None:
            idx = current_device()
        default_generator = torch.xpu.default_generators[idx]
        default_generator.set_state(new_state)

    _lazy_call(cb)

