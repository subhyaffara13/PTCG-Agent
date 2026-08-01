
def prepare_softmax_extra_check(match):
    """
    We only have triton online softmax kernels currently.
    """
    device_type = match.kwargs["x"].meta["val"].device.type
    return (
        config.online_softmax
        and device_type in ["cuda", "xpu"]
        and getattr(config, f"{device_type}_backend") == "triton"
    )

