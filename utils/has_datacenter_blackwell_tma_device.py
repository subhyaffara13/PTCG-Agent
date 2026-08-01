
def has_datacenter_blackwell_tma_device() -> bool:
    import torch

    if (
        torch.cuda.is_available()
        and torch.cuda.get_device_capability() >= (10, 0)
        and torch.cuda.get_device_capability() < (11, 0)
        and not torch.version.hip
    ):
        return has_triton_tma_device() and has_triton_tensor_descriptor_host_tma()

    return False

