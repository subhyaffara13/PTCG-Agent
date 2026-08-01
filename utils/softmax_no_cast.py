
def softmax_no_cast(t: torch.Tensor, dim: int = -1) -> torch.Tensor:
    """
    Softmax, but without automatic casting to fp32 when the input is of type bfloat16
    """
    d = t.dtype
    if d is torch.bfloat16 and not is_deepspeed_initialized():
        with maybe_autocast(device_type="cuda", enabled=False):
            s = torch.nn.functional.softmax(t, dim=dim)
    else:
        s = torch.nn.functional.softmax(t, dim=dim)

    return s

