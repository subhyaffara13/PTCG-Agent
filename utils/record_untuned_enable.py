
def record_untuned_enable(val: bool = True) -> None:
    r"""Enable recording untuned of TunableOp perations for offline tuning.

    When enabled, if a tuned entry isn't found, write it to the untuned file.
    """
    torch._C._cuda_record_untuned_enable(val)  # type: ignore[attr-defined]

