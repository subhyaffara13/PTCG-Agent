
def _rocm_native_device_arch_name(device: str) -> str:
    return torch.cuda.get_device_properties(device).gcnArchName

