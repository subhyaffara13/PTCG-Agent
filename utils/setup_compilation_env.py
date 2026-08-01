
def setup_compilation_env():
    """
    Context manager that sets up proper environment and backend when invoking torch.compile
    inside torch.export region or inside HOP.
    """
    from torch._dynamo.backends.debugging import (
        make_eager_backend_with_torch_function_modes,
    )
    from torch._dynamo.backends.registry import lookup_backend
    from torch.fx.experimental.proxy_tensor import (
        _temp_remove_pre_dispatch_torch_function_mode,
    )

    old_in_hop_compile = getattr(_hop_compile_tls, "in_hop_compile", False)
    _hop_compile_tls.in_hop_compile = True
    try:
        with (
            _set_compilation_env(),
            torch._dynamo.utils.disable_cache_limit(),
            _temp_remove_pre_dispatch_torch_function_mode() as pre_dispatch_mode,
            _temp_remove_metadata_torch_function_mode() as metadata_mode,
        ):
            modes = [
                mode for mode in (pre_dispatch_mode, metadata_mode) if mode is not None
            ]
            if modes:
                yield make_eager_backend_with_torch_function_modes(modes)
            else:
                yield lookup_backend("eager")
    finally:
        _hop_compile_tls.in_hop_compile = old_in_hop_compile

