
def _unshard_grads(
    handle: FlatParamHandle | None,
) -> None:
    if handle:
        handle.unshard_grad()

