
def all_gather_merge_fn_to_trace(
    ag_ins: list[torch.Tensor],
    group_size: int,
    group_name: str,
    dtype: torch.dtype,  # type: ignore[name-defined]
    out_dtypes: list[torch.dtype],  # type: ignore[name-defined]
    rank: int,
) -> list[torch.Tensor]:
    ins_sizes = [ag_in.shape for ag_in in ag_ins]
    ins_split_sizes = [ag_in.numel() for ag_in in ag_ins]
    ag_input_numel = sum(ins_split_sizes)
    device = ag_ins[0].device
    new_ag_out = torch.empty(ag_input_numel * group_size, dtype=dtype, device=device)
    new_ag_in = new_ag_out.narrow(0, ag_input_numel * rank, ag_input_numel)
    ag_ins_flattened = [ag_in.reshape(-1) for ag_in in ag_ins]
    # Inductor fuses copy_(cat(...)) into 1 Triton kernel with no allocation for cat.
    # _foreach_copy_(..., ag_ins_flattened) emits separate kernel per item,
    # resulting in large number of small triton kernels to launch.
    new_ag_in.copy_(torch.cat(ag_ins_flattened))
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

