
def get_default_kpack(block_k: int = 16) -> int:
    if not torch.version.hip:
        return 0
    if "gfx942" in torch.cuda.get_device_properties(0).gcnArchName and block_k <= 16:
        return 1
    return 2

