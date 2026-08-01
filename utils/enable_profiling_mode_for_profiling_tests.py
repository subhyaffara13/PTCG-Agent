
def enable_profiling_mode_for_profiling_tests():
    old_prof_exec_state = False
    old_prof_mode_state = False
    if not GRAPH_EXECUTOR:
        raise AssertionError("GRAPH_EXECUTOR must be set")
    if GRAPH_EXECUTOR == ProfilingMode.PROFILING:
        old_prof_exec_state = torch._C._jit_set_profiling_executor(True)
        old_prof_mode_state = torch._C._get_graph_executor_optimize(True)
    try:
        yield
    finally:
        if GRAPH_EXECUTOR == ProfilingMode.PROFILING:
            torch._C._jit_set_profiling_executor(old_prof_exec_state)
            torch._C._get_graph_executor_optimize(old_prof_mode_state)

