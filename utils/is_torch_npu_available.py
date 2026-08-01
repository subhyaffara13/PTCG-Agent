
def is_torch_npu_available(check_device=False) -> bool:
    "Checks if `torch_npu` is installed and potentially if a NPU is in the environment"
    if not is_torch_available() or not _is_package_available("torch_npu")[0]:
        return False

    import torch
    import torch_npu  # noqa: F401

    if check_device:
        try:
            # Will raise a RuntimeError if no NPU is found
            if hasattr(torch, "npu"):
                _ = torch.npu.device_count()
                return torch.npu.is_available()
            return False
        except RuntimeError:
            return False
    return hasattr(torch, "npu") and torch.npu.is_available()

