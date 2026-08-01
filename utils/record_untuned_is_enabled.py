
def record_untuned_is_enabled() -> bool:
    r"""Returns whether TunableOp operations are recorded for offline tuning."""
    return torch._C._cuda_record_untuned_is_enabled()  # type: ignore[attr-defined]

