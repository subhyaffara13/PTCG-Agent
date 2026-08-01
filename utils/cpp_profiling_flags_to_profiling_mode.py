
def cppProfilingFlagsToProfilingMode():
    old_prof_exec_state = torch._C._jit_set_profiling_executor(True)
    old_prof_mode_state = torch._C._get_graph_executor_optimize(True)
    torch._C._jit_set_profiling_executor(old_prof_exec_state)
    torch._C._get_graph_executor_optimize(old_prof_mode_state)

    if old_prof_exec_state:
        if old_prof_mode_state:
            return ProfilingMode.PROFILING
        else:
            return ProfilingMode.SIMPLE
    else:
        return ProfilingMode.LEGACY

