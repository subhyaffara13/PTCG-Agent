
def call_fork_with_profiling(record: torch.classes.profiler._RecordFunction) -> Tensor:
    # Call fork from within ScriptFunction and ensure that we can attach profiling
    # callbacks to the resulting future. Note that handle here is a Tensor
    # representation of RecordFunction.
    fut = torch.jit._fork(one_arg, torch.tensor(1))
    torch.ops.profiler._call_end_callbacks_on_jit_fut(record, fut)
    ret = fut.wait()
    return ret

