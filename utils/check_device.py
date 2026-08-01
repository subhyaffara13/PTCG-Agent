
def check_device(f_name, t, device):
    check(
        t.device == device and t.device.type == "cuda",
        f"{f_name}(): all inputs are expected to be on the same GPU device.",
    )


def check_device(a: Tensor, b: Tensor, device="cuda") -> bool:
    return (a.device.type == b.device.type) and (b.device.type == device)


def check_device(a: Tensor, b: Tensor) -> bool:
    return (a.is_cuda and b.is_cuda) or (a.is_xpu and b.is_xpu)

