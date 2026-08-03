from typing import Any

def _fused_all_gather_matmul_last_gather_dim_impl(
    mm_out_op: torch._ops.OpOverload,
    A_shard: torch.Tensor,
    Bs: list[torch.Tensor],
    A_scale: torch.Tensor | None,
    kwargs_list: list[dict[str, Any]],
    out_dtypes: list[torch.dtype | None],
    gather_dim: int,
    group_name: c10d.GroupName,
    return_A: bool,
) -> tuple[torch.Tensor | None, list[torch.Tensor]]:
    group = c10d._resolve_process_group(group_name)
    group_size = group.size()

    B_shards = [B.chunk(group.size()) for B in Bs]

    leading_dims = list(A_shard.shape[:-1])
    A_shard_flat = A_shard.flatten(0, -2)

    def unflatten(t: torch.Tensor) -> torch.Tensor:
        return t.view(*leading_dims, -1)

    A_flat_out = A_shard_flat.new_empty(
        A_shard_flat.shape[0] * group.size(),
        A_shard_flat.shape[1],
    )

    outputs = [
        torch.empty(
            (A_shard_flat.shape[0], B.shape[1]),
            dtype=out_dtype or B.dtype,
            device=A_shard.device,
        )
        for B, out_dtype in zip(Bs, out_dtypes)
    ]

    first = True
    events = [torch.cuda.Event() for _ in outputs]

    def default_consumer(shard: torch.Tensor, rank: int) -> None:
        nonlocal first
        for out, event, B_shard, kwargs in zip(outputs, events, B_shards, kwargs_list):
            event.wait()
            if first:
                torch.ops.aten.mm.out(shard, B_shard[rank], **kwargs, out=out)
            else:
                out.addmm_(shard, B_shard[rank])
            event.record()

        first = False

    _pipelined_all_gather_and_consume_last_dim(
        A_shard_flat,
        default_consumer,
        A_flat_out,
        group_name,
        return_A,
    )
    ret_A = None
    if return_A:
        # This path is inefficient and will be filtered out at passes stage
        # Added only for completeness.
        A_split_cat_out_flat = torch.cat(A_flat_out.chunk(group_size), dim=-1)
        ret_A = unflatten(A_split_cat_out_flat)

    return ret_A, [unflatten(output) for output in outputs]

