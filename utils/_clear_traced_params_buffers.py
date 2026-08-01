
def _clear_traced_params_buffers(
    traced_module: torch.fx.GraphModule, const_keys: Sequence[str]
) -> None:
    """Remove all parameters and buffers from traced module before restoring.

    For constants (parameters/buffers that don't need FQN mapping), this function
    removes them from the _buffers dict and re-assigns them as direct attributes.
    This ensures constants don't show up as buffers in the state dict.

    Args:
        traced_module: The traced GraphModule to clean up.
        const_keys: List of keys that represent constants to be cleared.
    """
    for key in const_keys:
        if key not in traced_module._buffers:
            raise AssertionError(f"Key {key} not found in traced_module._buffers")
        # We don't want constants to show up as a buffer in the state dict.
        # Instead they should just be a direct attribute.
        buffer = traced_module._buffers[key]
        del traced_module._buffers[key]
        # Note: setattr will register the value per nn.Module rules:
        # - If it's a Tensor, it'll be re-registered as a buffer (ends up back in _buffers).
        # - Otherwise, it becomes a plain attribute (not part of state_dict).
        setattr(traced_module, key, buffer)

