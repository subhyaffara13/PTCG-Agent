
def all_gather_merge_fn_to_trace_functional(
    ag_ins: list[torch.Tensor],
    group_size: int,
    group_name: str,
    dtype: torch.dtype,  # type: ignore[name-defined]
    out_dtypes: list[torch.dtype],  # type: ignore[name-defined]
    rank: int,
    use_fsdp_ag_copy_in: bool = False,
) -> list[torch.Tensor]:
    # Implementation that is functional in graph,
    # but uses custom op torch.ops.fsdp.all_gather_copy_in.
    ins_sizes = [ag_in.shape for ag_in in ag_ins]
    ins_split_sizes = [ag_in.numel() for ag_in in ag_ins]
    ag_input_numel = sum(ins_split_sizes)
    device = ag_ins[0].device
    new_ag_out = torch.empty(ag_input_numel * group_size, dtype=dtype, device=device)
    ag_ins_flattened = [ag_in.reshape(-1) for ag_in in ag_ins]
    if use_fsdp_ag_copy_in:
        new_ag_in, new_ag_out = torch.ops.fsdp.all_gather_copy_in(
            ag_ins_flattened, new_ag_out, ins_split_sizes, ag_input_numel, rank
        )
    else:
        new_ag_in = torch.cat(ag_ins_flattened, dim=0)
    wait_tensor = torch.ops.c10d_functional.wait_tensor(
        torch.ops._c10d_functional.all_gather_into_tensor_out.default(
            new_ag_in, group_size, group_name, out=new_ag_out
        )
    )
    new_ag_out_reshaped = wait_tensor.reshape(group_size, -1)
    outs = torch.split_with_sizes(
        new_ag_out_reshaped,
        ins_split_sizes,
        dim=1,
    )
    outs_reshaped = [
        o.reshape((shape[0] * group_size,) + shape[1:])
        for o, shape in zip(outs, ins_sizes)
    ]
    return outs_reshaped

