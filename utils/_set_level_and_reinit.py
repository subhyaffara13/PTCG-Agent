
def _setLevel_and_reinit(level: int) -> None:
    _orig_setLevel(level)
    torch._C._reinit_DTensor_dispatch_logger()

