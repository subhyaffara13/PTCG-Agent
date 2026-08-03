from typing import Any

def get_device_properties() -> DeviceProperties:
    """
    Get environment device properties.
    """
    if IS_CUDA_SYSTEM or IS_ROCM_SYSTEM:
        import torch

        if torch.cuda.is_available():
            major, minor = torch.cuda.get_device_capability()
            if IS_ROCM_SYSTEM:
                return ("rocm", major, minor)
            else:
                return ("cuda", major, minor)
    if IS_XPU_SYSTEM:
        import torch

        if torch.xpu.is_available():
            # To get more info of the architecture meaning and bit allocation, refer to https://github.com/intel/llvm/blob/sycl/sycl/include/sycl/ext/oneapi/experimental/device_architecture.def
            arch = torch.xpu.get_device_capability()["architecture"]
            gen_mask = 0x000000FF00000000
            gen = (arch & gen_mask) >> 32
            return ("xpu", gen, None)
    if IS_NPU_SYSTEM:
        # TODO: after torch 2.5.1, use `if hasattr(torch, "npu") and torch.npu.is_available()` here for consistency with CUDA/XPU blocks
        return ("npu", None, None)
    return (torch_device, None, None)


def get_device_properties(device: Device = None) -> _CudaDeviceProperties:
    r"""Get the properties of a device.

    Args:
        device (torch.device or int or str, optional): device for which to return the
            properties of the device.  It uses the current device, given by
            :func:`~torch.cuda.current_device`, if :attr:`device` is ``None``
            (default).

    Returns:
        _CudaDeviceProperties: the properties of the device
    """
    _lazy_init()  # will define _get_device_properties
    device = _get_device_index(device, optional=True)
    if device < 0 or device >= device_count():
        raise AssertionError("Invalid device id")
    return _get_device_properties(device)  # type: ignore[name-defined]


def get_device_properties(device: Device = None) -> dict[str, Any]:
    r"""Return a dictionary of MTIA device properties

    Args:
        device (torch.device or int, optional) selected device. Returns
            statistics for the current device, given by current_device(),
            if device is None (default).
    """
    return torch._C._mtia_getDeviceProperties(_get_device_index(device, optional=True))


def get_device_properties(
    device: Device = None,
) -> _XpuDeviceProperties:
    r"""Get the properties of a device. Returns _XpuDeviceProperties containing the following device properties:

    - ``name`` (str): device name.
    - ``platform_name`` (str): SYCL platform name.
    - ``vendor`` (str): device vendor.
    - ``device_id`` (int): device identifier (product ID).
    - ``driver_version`` (str): driver version.
    - ``version`` (str): runtime version.
    - ``max_compute_units`` (int): number of parallel compute units.
    - ``gpu_eu_count`` (int): number of EUs (Execution Unit).
    - ``max_work_group_size``: (int): maximum number of work-items permitted in a work-group.
    - ``max_num_sub_groups`` (int): maximum number of sub-groups supported in a work-group.
    - ``memory_clock_rate`` (int) maximum clock rate of device's global memory in MHz.
    - ``memory_bus_width`` (int) maximum bus width between device and memory in bits.
    - ``sub_group_sizes``: (list[int]): a list of supported sub-group sizes.
    - ``local_mem_size`` (int): device local memory capacity that can be allocated per work-group in bytes.
    - ``has_fp16`` (bool): whether float16 dtype is supported.
    - ``has_fp64`` (bool): whether float64 dtype is supported.
    - ``has_atomic64`` (bool): whether 64-bit atomic operations are supported.
    - ``has_bfloat16_conversions`` (bool): whether bfloat16 conversions are supported.
    - ``has_subgroup_matrix_multiply_accumulate`` (bool): whether DPAS (Dot Product Accumulate Systolic) is supported.
    - ``has_subgroup_matrix_multiply_accumulate_tensor_float32`` (bool): whether DPAS with tf32 inputs is supported.
    - ``has_subgroup_2d_block_io`` (bool): whether 2D block I/O for efficient matrix multiplication is supported.
    - ``total_memory`` (int): device global memory in bytes.
    - ``gpu_subslice_count`` (int): number of subslice.
    - ``architecture`` (int): device architecture identifier (experimental).
    - ``type`` (str): device type, e.g. 'cpu', 'gpu', accelerator', 'host', 'unknown'.
    - ``uuid`` (Any): device UUID (Universal Unique ID), 16 bytes.

    Args:
        device (torch.device or int or str): device for which to return the
            properties of the device.

    Returns:
        _XpuDeviceProperties: the properties of the device
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    return _get_device_properties(device)  # type: ignore[name-defined]  # noqa: F821

