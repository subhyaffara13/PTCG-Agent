
def _maybe_handle_skip_if_lt_x_gpu(args, msg) -> bool:
    _handle_test_skip = getattr(args[0], "_handle_test_skip", None)
    if len(args) == 0 or _handle_test_skip is None:
        return False
    _handle_test_skip(msg)
    return True

