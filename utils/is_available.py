import copy

def is_available() -> bool:
    r"""Check if the current accelerator is available at runtime: it was build, all the
    required drivers are available and at least one device is visible.
    See :ref:`accelerator<accelerators>` for details.

    Returns:
        bool: A boolean indicating if there is an available :ref:`accelerator<accelerators>`.

    .. note:: This API delegates to the device-specific version of `is_available`.
        On CUDA, when the environment variable ``PYTORCH_NVML_BASED_CUDA_CHECK=1`` is set,
        this function will NOT poison fork. Otherwise, it will. For more details, see
        :ref:`multiprocessing-poison-fork-note`.

    Example::

        >>> assert torch.accelerator.is_available() "No available accelerators detected."
    """
    # Why not just check "device_count() > 0" like other is_available call?
    # Because device like CUDA have a python implementation of is_available that is
    # non-poisoning and some features like Dataloader rely on it.
    # So we are careful to delegate to the Python version of the accelerator here
    acc = current_accelerator()
    if acc is None:
        return False

    mod = torch.get_device_module(acc)
    return mod.is_available()


def is_available() -> bool:
    r"""Returns a bool indicating if CPU is currently available.

    N.B. This function only exists to facilitate device-agnostic code

    """
    return True


def is_available(tensors):
    if not hasattr(torch._C, "_nccl_all_reduce"):
        warnings.warn("PyTorch is not compiled with NCCL support", stacklevel=2)
        return False

    devices = set()
    for tensor in tensors:
        if tensor.is_sparse:
            return False
        if not tensor.is_contiguous():
            return False
        if not tensor.is_cuda:
            return False
        device = tensor.get_device()
        if device in devices:
            return False
        devices.add(device)

    return True


def is_available() -> bool:
    r"""
    Return a bool indicating if CUDA is currently available.

    .. note:: This function will NOT poison fork if the environment variable
        ``PYTORCH_NVML_BASED_CUDA_CHECK=1`` is set. For more details, see
        :ref:`multiprocessing-poison-fork-note`.
    """
    if not _is_compiled():
        return False
    if _nvml_based_avail():
        # The user has set an env variable to request this availability check that attempts to avoid fork poisoning by
        # using NVML at the cost of a weaker CUDA availability assessment. Note that if NVML discovery/initialization
        # fails, this assessment falls back to the default CUDA Runtime API assessment (`cudaGetDeviceCount`)
        return device_count() > 0
    else:
        # The default availability inspection never throws and returns 0 if the driver is missing or can't
        # be initialized. This uses the CUDA Runtime API `cudaGetDeviceCount` which in turn initializes the CUDA Driver
        # API via `cuInit`
        return torch._C._cuda_getDeviceCount() > 0


def is_available() -> bool:
    """
    Return ``True`` if the distributed package is available.

    Otherwise,
    ``torch.distributed`` does not expose any other APIs. Currently,
    ``torch.distributed`` is available on Linux, MacOS and Windows. Set
    ``USE_DISTRIBUTED=1`` to enable it when building PyTorch from source.
    Currently, the default value is ``USE_DISTRIBUTED=1`` for Linux and Windows,
    ``USE_DISTRIBUTED=0`` for MacOS.
    """
    return hasattr(torch._C, "_c10d_init")


def is_available() -> bool:
    return device_count() > 0


def is_available() -> bool:
    r"""Return true if MTIA device is available"""
    if not _is_compiled():
        return False
    # MTIA has to init devices first to know if there is any devices available.
    return device_count() > 0


def is_available():
    """
    Check if ITT feature is available or not
    """
    return _itt.is_available()


def is_available() -> bool:
    r"""Return a bool indicating if XPU is currently available."""
    # This function never throws.
    return device_count() > 0


def is_available() -> bool:
    return hasattr(torch._C, "_dist_autograd_init")


def is_available() -> bool:
    return hasattr(torch._C, "_rpc_init")


def is_available() -> bool:
    return hasattr(torch._C, "_faulty_agent_init")


def is_available():
    r"""Return a bool indicating if CUDNN is currently available."""
    return torch._C._has_cudnn


def is_available() -> bool:
    r"""Return a bool indicating if cuSPARSELt is currently available."""
    return torch._C._has_cusparselt


def is_available():
    r"""Return whether PyTorch is built with KleidiAI support."""
    return torch._C._has_kleidiai


def is_available():
    r"""Return whether PyTorch is built with MKL support."""
    return torch._C.has_mkl


def is_available():
    r"""Return whether PyTorch is built with MKL-DNN support."""
    return torch._C._has_mkldnn


def is_available() -> bool:
    r"""Return a bool indicating if MPS is currently available."""
    return torch._C._mps_is_available()


def is_available():
    r"""Return whether PyTorch is built with NNPACK support."""
    return torch._nnpack_available()


def is_available():
    r"""Return whether PyTorch is built with OpenMP support."""
    return torch._C.has_openmp


def is_available() -> bool:
    r"""Return a bool indicating if opt_einsum is currently available.

    You must install opt-einsum in order for torch to automatically optimize einsum. To
    make opt-einsum available, you can install it along with torch: ``pip install torch[opt-einsum]``
    or by itself: ``pip install opt-einsum``. If the package is installed, torch will import
    it automatically and use it accordingly. Use this function to check whether opt-einsum
    was installed and properly imported by torch.
    """
    return _opt_einsum is not None


def is_available() -> bool:
    return copy != lazy_load_stub_copy and paste != lazy_load_stub_paste

