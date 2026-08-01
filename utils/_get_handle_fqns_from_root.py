
def _get_handle_fqns_from_root(
    state: _FSDPState, handle: "FlatParamHandle"
) -> list[str] | None:
    if handle is None:
        return None
    param_to_fqn = state._exec_order_data.param_to_fqn
    handle_params = handle.flat_param._params  # only populated for use_orig_params
    param_fqns = [*chain.from_iterable(param_to_fqn[p] for p in handle_params)]
    return param_fqns

