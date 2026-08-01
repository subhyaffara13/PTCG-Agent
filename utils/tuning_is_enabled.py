
def tuning_is_enabled() -> bool:
    r"""Returns whether TunableOp implementations can be tuned."""
    return torch._C._cuda_tunableop_tuning_is_enabled()  # type: ignore[attr-defined]

