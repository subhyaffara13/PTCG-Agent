
def construct_rpc_backend_options(
    backend,
    rpc_timeout=rpc_constants.DEFAULT_RPC_TIMEOUT_SEC,
    init_method=rpc_constants.DEFAULT_INIT_METHOD,
    **kwargs,
):
    return backend.value.construct_rpc_backend_options_handler(
        rpc_timeout, init_method, **kwargs
    )

