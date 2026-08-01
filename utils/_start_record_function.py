
def _start_record_function(exec_type, func_name, current_worker_name, dest_worker_name):
    """
    This function should be called from RPC/RRef functions to create a
    RecordFunction object for profiling. This function also runs the before
    callbacks that start the profiling, though the user is responsible for
    running the appropriate callbacks when the function to be profiled finishes.

    Args:
        exec_type (RPCExecMode): Type of RPC/RRef call
        func_name (str): Name of function being profiled.
        current_worker_name (str): Name of current worker.
        dest_worker_name (str): Name of the destination worker.

    Returns:
        An instance of `torch.autograd._RecordFunction`.
    """
    if not torch.autograd._profiler_enabled():
        raise AssertionError("Autograd profiler should be enabled.")
    profile_key = f"rpc_{exec_type.value}#{str(func_name)}({current_worker_name} -> {dest_worker_name})"
    rf = torch.autograd._RecordFunction()  # type: ignore[attr-defined]
    torch.autograd._run_before_callbacks(rf, profile_key)  # type: ignore[attr-defined]
    return rf

