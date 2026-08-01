
def _set_autograd_backward(enable: bool = True) -> Iterator[None]:
    global current_meta

    had_autograd_backward = "autograd_backward" in current_meta
    old_autograd_backward = current_meta.get("autograd_backward", False)

    if enable:
        _mark_autograd_backward()
    try:
        yield
    finally:
        if had_autograd_backward:
            current_meta["autograd_backward"] = old_autograd_backward
        else:
            _reset_autograd_backward()

