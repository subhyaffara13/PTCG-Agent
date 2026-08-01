
def _get_registry_functions():
    """Lazy import of registry functions."""
    from torch._native.registry import (
        _filter_state,
        _graphs,
        deregister_op_overrides,
        reenable_op_overrides,
    )

    return deregister_op_overrides, reenable_op_overrides, _graphs, _filter_state

