
def record_pregraph_bytecode_enter() -> AbstractContextManager[None]:
    cm: AbstractContextManager[None] = (
        torch._C._profiler._RecordFunctionFast("Pregraph bytecode")
        if torch.autograd.profiler._is_profiler_enabled
        else contextlib.nullcontext()
    )
    cm.__enter__()
    return cm

