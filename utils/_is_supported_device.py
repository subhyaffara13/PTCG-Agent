
def _is_supported_device(tensor: torch.Tensor) -> bool:
    return tensor.is_cuda or tensor.device.type in (
        "xla",
        "cpu",
        "hpu",
        "mtia",
        "xpu",
        torch._C._get_privateuse1_backend_name(),
    )

