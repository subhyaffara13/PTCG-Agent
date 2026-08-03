from typing import Callable

def _pipelined_all_gather_and_consume(
    shard: torch.Tensor,
    shard_consumer: Callable[[torch.Tensor, int], None],
    ag_out: torch.Tensor,
    group_name: c10d.GroupName,
    ag_out_needed: bool = True,
) -> None:
    """
    Perform the following logic with micro-pipelined computation and
    communication:

        ag_out = all_gather_tensor(shard, gather_dim=0, group=group)
        shards = ag_out.chunk(group.size())
        for src_rank, shard in enumerate(shards):
            shard_consumer(shard, src_rank)
    """

    def adapter(shard: list[torch.Tensor], rank: int) -> None:
        shard_consumer(shard[0], rank)

    _pipelined_multi_all_gather_and_consume(
        [shard],
        adapter,
        [ag_out],
        group_name,
        ag_out_needed,
    )

