
def _local_recv_(
    tensors: list[torch.Tensor],
    process_group_so: ScriptObject,
    src: int,
    tag: int,
) -> ScriptObject:
    # "recv_(Tensor[] tensors, __torch__.torch.classes.c10d.ProcessGroup process_group, "
    # "int src, int tag) -> __torch__.torch.classes.c10d.Work";
    from . import LocalRunnerMode, LocalTensor

    if len(tensors) != 1:
        raise AssertionError
    tensor = tensors[0]

    if not isinstance(tensor, LocalTensor):
        raise AssertionError("Input tensor must be a Tensor")
    dst = int(tensor.__src_rank__)

    def _recv_and_store(timeout: timedelta) -> bool:
        def _wait_and_store(obj: object) -> None:
            if not isinstance(obj, torch.Tensor):
                raise AssertionError("Expected to receive a Tensor")
            if not isinstance(tensor, LocalTensor):
                raise AssertionError("Input tensor must be a Tensor")
            tensor._local_tensors[dst] = obj

        LocalRunnerMode.current()._wait_recv(src, dst, _wait_and_store)
        return True

    work = PythonCallbackWork(_recv_and_store)
    work_so = Work.boxed(work)
    return work_so

