import copy
import sys

def _check_device(bare_xp: Namespace, device: Device) -> None:  # pyright: ignore[reportUnusedFunction]
    """
    Validate dummy device on device-less array backends.

    Notes
    -----
    This function is also invoked by CuPy, which does have multiple devices
    if there are multiple GPUs available.
    However, CuPy multi-device support is currently impossible
    without using the global device or a context manager:

    https://github.com/data-apis/array-api-compat/pull/293
    """
    if bare_xp is sys.modules.get("numpy"):
        if device not in ("cpu", None):
            raise ValueError(f"Unsupported device for NumPy: {device!r}")

    elif bare_xp is sys.modules.get("dask.array"):
        if device not in ("cpu", _DASK_DEVICE, None):
            raise ValueError(f"Unsupported device for Dask: {device!r}")


def _check_device(device, dlpack_device, copy):
  if device and dlpack_device != device:
    if copy is not None and not copy:
      raise ValueError(
        f"Specified {device=} which requires a copy since the source device "
        f"is {repr(dlpack_device)}, however copy=False. Set copy=True or "
        "copy=None to perform the requested operation."
      )

