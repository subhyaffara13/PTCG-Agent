
def _build_rpc_profiling_key(
    exec_type, func_name, current_worker_name, dst_worker_name
):
    """
    Builds the key that RPC calls are profiled with using the autograd profiler.
    This will be the name of the corresponding Event recorded in the profiler.

    Args:
        exec_type (RPCExecMode): Type of RPC/RRef call
        func_name (str): Name of function being profiled.
        current_worker_name (str): Name of current worker.
        dst_worker_name (str): Name of the destination worker.

    Returns:
        String representing profiling key
    """
    profile_key = (
        f"rpc_{exec_type.value}#{func_name}({current_worker_name} -> {dst_worker_name})"
    )
    return profile_key

