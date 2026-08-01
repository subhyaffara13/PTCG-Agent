
def enable(val: bool = True) -> None:
    r"""This is the big on/off switch for all TunableOp implementations."""
    torch._C._cuda_tunableop_enable(val)  # type: ignore[attr-defined]


def enable() -> None:
    _enabled.enabled = True

