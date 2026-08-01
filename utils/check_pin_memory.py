
def check_pin_memory(pin_memory: bool):
    torch._check_not_implemented(
        not pin_memory, lambda: "PrimTorch does not support pinned memory"
    )

