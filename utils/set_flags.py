
def set_flags(node: Node, flags: list[str]) -> None:
    for name in flags:
        setattr(node, name, True)


def set_flags(_fp32_precision="none"):
    orig_flags = (torch._C._get_fp32_precision_getter("generic", "all"),)
    if _fp32_precision is not None:
        torch._C._set_fp32_precision_setter("generic", "all", _fp32_precision)
    return orig_flags


def set_flags(
    _enabled=None,
    _benchmark=None,
    _benchmark_limit=None,
    _deterministic=None,
    _allow_tf32=None,
    _fp32_precision="none",
):
    orig_flags = (
        torch._C._get_cudnn_enabled(),
        torch._C._get_cudnn_benchmark(),
        None if not is_available() else torch._C._cuda_get_cudnn_benchmark_limit(),
        torch._C._get_cudnn_deterministic(),
        torch._C._get_cudnn_allow_tf32(),
        torch._C._get_fp32_precision_getter("cuda", "all"),
    )
    if _enabled is not None:
        torch._C._set_cudnn_enabled(_enabled)
    if _benchmark is not None:
        torch._C._set_cudnn_benchmark(_benchmark)
    if _benchmark_limit is not None and is_available():
        torch._C._cuda_set_cudnn_benchmark_limit(_benchmark_limit)
    if _deterministic is not None:
        torch._C._set_cudnn_deterministic(_deterministic)
    if _allow_tf32 is not None:
        torch._C._set_cudnn_allow_tf32(_allow_tf32)
    if _fp32_precision is not None:
        torch._C._set_fp32_precision_setter("cuda", "all", _fp32_precision)
    return orig_flags


def set_flags(
    _immediate=None,
):
    orig_flags = (torch._C._get_miopen_immediate(),)
    if _immediate is not None:
        torch._C._set_miopen_immediate(_immediate)
    return orig_flags


def set_flags(
    _enabled=None, _deterministic=None, _allow_tf32=None, _fp32_precision="none"
):
    orig_flags = (
        torch._C._get_mkldnn_enabled(),
        torch._C._get_mkldnn_deterministic(),
        torch._C._get_onednn_allow_tf32(),
        torch._C._get_fp32_precision_getter("mkldnn", "all"),
    )
    if _enabled is not None:
        torch._C._set_mkldnn_enabled(_enabled)
    if _deterministic is not None:
        torch._C._set_mkldnn_deterministic(_deterministic)
    if _allow_tf32 is not None:
        torch._C._set_onednn_allow_tf32(_allow_tf32)
    if _fp32_precision is not None:
        torch._C._set_fp32_precision_setter("mkldnn", "all", _fp32_precision)
    return orig_flags


def set_flags(_enabled):
    r"""Set if nnpack is enabled globally"""
    orig_flags = (torch._C._get_nnpack_enabled(),)
    torch._C._set_nnpack_enabled(_enabled)
    return orig_flags


def set_flags(_enabled=None, _strategy=None):
    orig_flags = (enabled, None if not is_available() else strategy)
    if _enabled is not None:
        _set_enabled(_enabled)
    if _strategy is not None:
        _set_strategy(_strategy)
    return orig_flags

