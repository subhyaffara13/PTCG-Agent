
def prof_callable(callable, *args, **kwargs):
    if 'profile_and_replay' in kwargs:
        del kwargs['profile_and_replay']
        if not GRAPH_EXECUTOR:
            raise AssertionError("GRAPH_EXECUTOR must be set")
        if GRAPH_EXECUTOR == ProfilingMode.PROFILING:
            with enable_profiling_mode_for_profiling_tests():
                callable(*args, **kwargs)
                return callable(*args, **kwargs)

    return callable(*args, **kwargs)

