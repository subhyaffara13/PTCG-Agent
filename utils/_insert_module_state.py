
def _insert_module_state(module: nn.Module, state: _State) -> None:
    global _module_state_mapping
    if module in _module_state_mapping:
        raise AssertionError(f"Inserting {module} more than once.")
    _module_state_mapping[module] = weakref.ref(state)

