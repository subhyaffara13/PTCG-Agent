import functools

def _require_initialized(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _is_current_rpc_agent_set():
            raise RuntimeError(
                "RPC has not been initialized. Call "
                "torch.distributed.rpc.init_rpc first."
            )
        return func(*args, **kwargs)

    return wrapper

