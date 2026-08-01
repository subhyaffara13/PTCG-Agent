
def requires_multicast_support():
    has_multicast_support = (
        torch.cuda.is_available()
        and _SymmetricMemory.has_multicast_support(DeviceType.CUDA, 0)
    )
    return skip_but_pass_in_sandcastle_if(
        not has_multicast_support,
        "multicast support is not available",
    )

