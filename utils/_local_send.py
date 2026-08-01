
def _local_send(
    tensors: list[torch.Tensor],
    process_group_so: ScriptObject,
    dst: int,
    tag: int,
) -> ScriptObject:
    # "send(Tensor[] tensors, __torch__.torch.classes.c10d.ProcessGroup process_group, "
    # "int dst, int tag) -> __torch__.torch.classes.c10d.Work";

    from . import LocalRunnerMode, LocalTensor

    if len(tensors) != 1:
        raise AssertionError
    tensor = tensors[0]

    if not isinstance(tensor, LocalTensor):
        raise AssertionError("Input tensor must be a Tensor")
    src = int(tensor.__src_rank__)

    LocalRunnerMode.current()._signal_send(src, dst, tensor._local_tensors[src])

    work = FakeWork()
    work_so = Work.boxed(work)
    return work_so

