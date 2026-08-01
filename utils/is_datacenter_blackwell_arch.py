
def is_datacenter_blackwell_arch() -> bool:
    arch = get_cuda_arch()
    if arch is None:
        return False
    arch_number = int(arch)
    return arch_number >= 100 and arch_number < 110

