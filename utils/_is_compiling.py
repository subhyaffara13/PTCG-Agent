
def _is_compiling(func, args, kwargs):
    # Check if we are under AOTAutograd tracing or export tracing
    # Checking that a proxy mode is active should always do what we want
    if torch.compiler._is_non_strict_tracing():
        return False
    return torch._C._get_dispatch_mode(torch._C._TorchDispatchModeKey.PROXY) is not None

