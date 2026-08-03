from typing import Any, Callable

def register_benchmarker(
    device_type: str,
    fn: Callable[..., Any],
    *,
    override: bool = False,
) -> None:
    """
    Register a device-type specific benchmarker.

    Args:
        device_type: torch.device.type string (e.g., "cuda", "cpu", "mps", "xpu").
        fn: callable(self, _callable, *, warmup, rep, **kwargs) -> Any
        override: allow overriding an existing registration.
    """
    if not isinstance(device_type, str) or not device_type:
        raise ValueError(
            "device_type must be a non-empty string matching torch.device.type"
        )
    if not callable(fn):
        raise TypeError("fn must be callable")
    if not override and device_type in _BENCHMARK_DISPATCH:
        raise ValueError(
            f"Benchmarker for device_type '{device_type}' already registered"
        )
    _BENCHMARK_DISPATCH[device_type] = fn

