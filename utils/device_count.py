
def device_count() -> int:
    r"""Return the number of current :ref:`accelerator<accelerators>` available.

    Returns:
        int: the number of the current :ref:`accelerator<accelerators>` available.
            If there is no available accelerators, return 0.

    .. note:: This API delegates to the device-specific version of `device_count`.
        On CUDA, this API will NOT poison fork if NVML discovery succeeds.
        Otherwise, it will. For more details, see :ref:`multiprocessing-poison-fork-note`.
    """
    acc = current_accelerator()
    if acc is None:
        return 0

    mod = torch.get_device_module(acc)
    return mod.device_count()


def device_count() -> int:
    r"""Returns number of CPU devices (not cores). Always 1.

    N.B. This function only exists to facilitate device-agnostic code
    """
    return 1


def device_count() -> int:
    r"""
    Return the number of GPUs available.

    .. note:: This API will NOT poison fork if NVML discovery succeeds.
        See :ref:`multiprocessing-poison-fork-note` for more details.
    """
    global _cached_device_count
    if not _is_compiled():
        return 0
    if _cached_device_count is not None:
        return _cached_device_count
    if _initialized or hasattr(_tls, "is_initializing"):
        r = torch._C._cuda_getDeviceCount()
    else:
        # bypass _device_count_nvml() if rocm (not supported)
        if torch.version.hip:
            nvml_count = _device_count_amdsmi()
        else:
            nvml_count = _device_count_nvml()
        r = torch._C._cuda_getDeviceCount() if nvml_count < 0 else nvml_count
    # NB: Do not cache the device count prior to CUDA initialization, because
    # the number of devices can change due to changes to CUDA_VISIBLE_DEVICES
    # setting prior to CUDA initialization.
    if _initialized:
        _cached_device_count = r
    return r


def device_count() -> int:
    r"""Returns the number of available MPS devices."""
    return int(torch._C._has_mps and torch._C._mps_is_available())


def device_count() -> int:
    r"""Return the number of MTIA devices available."""
    return torch._C._mtia_getDeviceCount()


def device_count() -> int:
    r"""Return the number of XPU device available."""
    if not _is_compiled():
        return 0
    return torch._C._xpu_getDeviceCount()


def device_count(
    backend: str | xla_client.Client | None = None
) -> int:
  """Returns the total number of devices.

  On most platforms, this is the same as :py:func:`jax.local_device_count`.
  However, on multi-process platforms where different devices are associated
  with different processes, this will return the total number of devices across
  all processes.

  Args:
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the xla backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.

  Returns:
    Number of devices.

  """
  return int(get_backend(backend).device_count())

