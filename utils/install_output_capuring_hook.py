
def install_output_capuring_hook(
    module: nn.Module, key: str, index: int, capture_initial_hidden_state: bool = True
) -> None:
    """Install the forward hook needed to capture the output described by `key` and `index` in `module`."""

    def output_capturing_hook(module, args, output):
        # Get the current thread-local collector
        collected_outputs = _active_collector.get()
        # If it's None or not a key we want to capture, simply return, the hook is inactive
        if collected_outputs is None or key not in collected_outputs.keys():
            return

        if capture_initial_hidden_state and key == "hidden_states" and len(collected_outputs[key]) == 0:
            collected_outputs[key].append(args[0])
        if not isinstance(output, tuple):
            collected_outputs[key].append(output)
        elif output[index] is not None:
            collected_outputs[key].append(output[index])

    module.register_forward_hook(output_capturing_hook)

