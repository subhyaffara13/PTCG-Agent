
def _is_composable(state: _FSDPState):
    # TODO: This is a temporary hack for differentiate between code paths.
    return not isinstance(state, nn.Module)

