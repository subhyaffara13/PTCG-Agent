
def _mark_autograd_backward() -> None:
    global current_meta

    current_meta["autograd_backward"] = True

