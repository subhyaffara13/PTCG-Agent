
def meta_histc(input, bins=100, min=0, max=0):
    fn_name = "histc()"
    if device_hint(input) == "cpu":
        torch._check(
            input.is_floating_point(),
            lambda: f"\"histogram_cpu\" not implemented for '{input.dtype}'",
        )
    if device_hint(input) == "cuda" and input.is_floating_point():
        utils.alert_not_deterministic("_histc_cuda with floating point input")
    torch._check(
        isinstance(bins, IntLike),
        lambda: f"{fn_name}: argument 'bins' must be int, not {type(bins)}",
    )
    torch._check(bins > 0, lambda: f"{fn_name}: bins must be > 0, but got {bins}")
    torch._check(
        isinstance(min, Number),
        lambda: f"{fn_name}: argument 'min' must be Number, not {type(min)}",
    )
    torch._check(
        isinstance(max, Number),
        lambda: f"{fn_name}: argument 'max' must be Number, not {type(max)}",
    )
    torch._check(max >= min, lambda: f"{fn_name}: max must be larger than min")
    return torch.empty(bins, device=input.device, dtype=input.dtype)

