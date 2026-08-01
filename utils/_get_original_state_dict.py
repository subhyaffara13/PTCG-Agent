
def _get_original_state_dict(mod: torch.nn.Module) -> dict[str, Any]:
    # Explicitly not calling mode.state_dict() as we do not want the module state for serialization
    # but the running module state so we can always match by id() the entries here with the graph inputs
    named_parameters = dict(mod.named_parameters(remove_duplicate=False))
    named_buffers = dict(mod.named_buffers(remove_duplicate=False))
    original_state_dict = named_parameters | named_buffers

    non_persistent_buffers = _get_non_persistent_buffers(mod)
    for k in non_persistent_buffers:
        original_state_dict.pop(k, None)

    return original_state_dict

