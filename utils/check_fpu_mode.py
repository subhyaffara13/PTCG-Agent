
def check_fpu_mode(request):
    """
    Check FPU precision mode was not changed during the test.
    """
    old_mode = get_fpu_mode()
    yield
    new_mode = get_fpu_mode()

    if old_mode != new_mode:
        raise AssertionError(f"FPU precision mode changed from {old_mode:#x} to "
                             f"{new_mode:#x} during the test")

    collect_result = _collect_results.get(request.node)
    if collect_result is not None:
        old_mode, new_mode = collect_result
        raise AssertionError(f"FPU precision mode changed from {old_mode:#x} to "
                             f"{new_mode:#x} when collecting the test")


def check_fpu_mode(request):
    """
    Check FPU mode was not changed during the test.
    """
    old_mode = get_fpu_mode()
    yield
    new_mode = get_fpu_mode()

    if old_mode != new_mode:
        warnings.warn(f"FPU mode changed from {old_mode:#x} to {new_mode:#x} during "
                      "the test",
                      category=FPUModeChangeWarning, stacklevel=0)

