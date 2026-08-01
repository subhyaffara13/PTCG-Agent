
def __setstate__(state: dict[str, Any]) -> dict[str, Any]:
    g = globals()
    for k, v in state.items():
        g['_sset_' + _state_vars[k]](k, g[k], v)
    return state

