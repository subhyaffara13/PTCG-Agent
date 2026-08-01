
def _check_tuning_assertions() -> None:
    r"""Helper function for multi-GPU tuning case. Need to check that TunableOp feature
    is enabled and that tuning is enabled.
    """

    if is_enabled() is False:
        warnings.warn("TunableOp was disabled. Trying to enable now.", stacklevel=2)
        enable(True)
    if is_enabled() is not True:
        raise AssertionError("is_enabled() must be True")
    if tuning_is_enabled() is not True:
        raise AssertionError("tuning_is_enabled() must be True")
    if record_untuned_is_enabled() is not False:
        raise AssertionError("record_untuned_is_enabled() must be False")

