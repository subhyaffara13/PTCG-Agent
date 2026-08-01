
def _is_in_fake_tensor_mode() -> bool:
    return any(
        isinstance(mode, FakeTensorMode) for mode in _get_current_dispatch_mode_stack()
    )

