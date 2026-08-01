
def _check_arg_device(x: torch.Tensor | None) -> bool:
    if x is not None:
        return x.device.type in [
            "cpu",
            "cuda",
            torch.utils.backend_registration._privateuse1_backend_name,
        ]
    return True

