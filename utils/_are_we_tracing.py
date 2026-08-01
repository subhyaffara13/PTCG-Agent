
def _are_we_tracing() -> bool:
    if is_torchdynamo_compiling():
        return True
    # If fake mode is turned on, we are almost definitely compiling/tracing.
    if torch._C._get_dispatch_mode(torch._C._TorchDispatchModeKey.FAKE) is not None:
        return True
    # See Note [enable_python_dispatcher in dynamo]
    if torch._C._dispatch_tls_is_dispatch_key_included(
        torch._C.DispatchKey.PythonDispatcher
    ):
        return True
    return get_proxy_mode() is not None

