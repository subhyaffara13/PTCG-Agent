
def call_rpc_with_profiling(
    record: torch.classes.profiler._RecordFunction, dst_worker_name: str
) -> Tensor:
    # Call rpc_async from within ScriptFunction and ensure that we can attach
    # profiling callbacks. Note that handle here is a Tensor representation of
    # RecordFunction.
    fut = rpc.rpc_async(dst_worker_name, one_arg, (torch.tensor(1),))
    torch.ops.profiler._call_end_callbacks_on_jit_fut(record, fut)
    ret = fut.wait()
    return ret

