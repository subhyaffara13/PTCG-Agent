
def reduce_scatter_merge_fn_coalesced(
    rs_ins: list[torch.Tensor],
    group_size: int,
    group_name: str,
    reduce_op: str,
    reduce_dtype: torch.dtype,
    device: torch.device,
) -> list[torch.Tensor]:
    """Bucketed RS via NCCL's coalesced API (ncclGroupStart/End).

    Avoids cat-ing inputs into one buffer; instead passes the tensor list
    directly to reduce_scatter_tensor_coalesced for zero-copy batching.
    """
    rs_ins_flat = [x.view(-1) for x in rs_ins]
    new_out_sizes = [(x.shape[0] // group_size,) + x.shape[1:] for x in rs_ins]

    rs_outs = torch.ops._c10d_functional.reduce_scatter_tensor_coalesced(
        rs_ins_flat, reduce_op, group_size, group_name
    )
    rs_outs = [torch.ops.c10d_functional.wait_tensor(o) for o in rs_outs]
    return [o.view(s) for o, s in zip(rs_outs, new_out_sizes)]

