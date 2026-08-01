
def should_unwrap_unspec_arg(name: str):
    if V.graph.is_unspec_arg(name):
        # Unwrap on all devices except CPU
        if V.graph.get_current_device_or_throw().type != "cpu":
            return True
        # Only unwrap on CPU if the input is not used as an output
        if name not in V.graph.mutated_buffers:
            return True
    return False

