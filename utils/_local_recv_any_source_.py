
def _local_recv_any_source_(
    tensors: list[torch.Tensor], process_group_so: ScriptObject, tag: int
) -> ScriptObject:
    # "recv_any_source_(Tensor[] tensors, __torch__.torch.classes.c10d.ProcessGroup process_group, "
    # "int tag) -> __torch__.torch.classes.c10d.Work";

    return _local_recv_(tensors, process_group_so, -1, tag)

