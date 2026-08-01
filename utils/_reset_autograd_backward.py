
def _reset_autograd_backward() -> None:
    global current_meta

    current_meta.pop("autograd_backward", None)

