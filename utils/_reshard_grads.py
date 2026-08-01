
def _reshard_grads(
    handle: FlatParamHandle | None,
) -> None:
    if handle:
        handle.reshard_grad()

