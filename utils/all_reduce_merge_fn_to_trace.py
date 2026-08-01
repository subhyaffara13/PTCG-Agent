
def all_reduce_merge_fn_to_trace(
    ar_ins: list[torch.Tensor],
    group_name: str,
    reduce_op: str,
    reduce_dtype: torch.dtype,  # type: ignore[name-defined]
    device: torch.device,  # type: ignore[name-defined]
) -> list[torch.Tensor]:  # type: ignore[no-untyped-def]
    ar_ins_flattened = [x.view(-1) for x in ar_ins]
    new_ar_in = torch.cat(ar_ins_flattened)
    new_ar_out = torch.ops.c10d_functional.wait_tensor(
        torch.ops._c10d_functional.all_reduce.default(new_ar_in, reduce_op, group_name)
    )
    split_sizes = [x.numel() for x in ar_ins]
    new_outs_flat = new_ar_out.split(split_sizes)
    new_outs = [x.view(ar_in.shape) for x, ar_in in zip(new_outs_flat, ar_ins)]
    return new_outs

