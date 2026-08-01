
def _local_gather_(
    output_tensors: list[list[torch.Tensor]],
    input_tensors: list[torch.Tensor],
    process_group_so: ScriptObject,
    root_rank: int,
    async_op: bool = True,
    timeout: int = -1,
) -> ScriptObject:
    # "gather_(Tensor[][] output_tensors, Tensor[] input_tensors, "
    # "__torch__.torch.classes.c10d.ProcessGroup process_group, int root_rank, "
    # "bool async_op=True, int timeout=-1) -> __torch__.torch.classes.c10d.Work"
    raise NotImplementedError(
        "LocalTensor does not support MPMD operations like gather "
        "(only root rank receives data). Use SPMD collective operations like allgather instead."
    )

