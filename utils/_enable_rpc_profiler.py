
def _enable_rpc_profiler(
    should_profile, qualified_name, func, rpc_type, dst_worker_info
):
    ctx_manager = contextlib.nullcontext()

    if should_profile:
        # Create appropriate string representation based on type of func
        # (builtin, script, python)
        if qualified_name is None:
            func_name = (
                torch._jit_internal._qualified_name(func)
                if isinstance(func, torch.jit.ScriptFunction)
                else func.__qualname__
            )
        else:
            func_name = qualified_name
        # Build RPC profiling key.
        rpc_profiling_key = _build_rpc_profiling_key(
            rpc_type,
            func_name,
            get_worker_info().name,
            dst_worker_info.name,
        )
        RemoteProfilerManager.set_current_profiling_key(rpc_profiling_key)
        # Mypy doesn't support re-def of a variable not in the same block (#1174)
        ctx_manager = torch.autograd.profiler.record_function(rpc_profiling_key)  # type: ignore[assignment]

    return ctx_manager

