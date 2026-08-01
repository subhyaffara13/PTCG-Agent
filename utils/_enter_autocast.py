
def _enter_autocast(*vals):
    # For pre-dispatch tracing, if a TorchFunction mode is active, we'll want to trace this into a graph.
    if torch._C._is_torch_function_mode_enabled():
        return torch.overrides.handle_torch_function(
            torch.amp._enter_autocast, [], *vals
        )
    mode = _UnmanagedAutocast(*vals)
    mode.__enter__()
    return mode

