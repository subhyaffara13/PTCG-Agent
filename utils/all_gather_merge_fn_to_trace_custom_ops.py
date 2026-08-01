
def all_gather_merge_fn_to_trace_custom_ops(
    _ag_ins: list[torch.Tensor],
    group_size: int,
    group_name: str,
    dtype: torch.dtype,  # type: ignore[name-defined]
    out_dtypes: list[torch.dtype],  # type: ignore[name-defined]
    rank: int,
) -> list[torch.Tensor]:
    # Don't create convert_element_type ops - _pre_bucket_all_gather handles conversion
    # by viewing destination slices as output dtypes and letting copy do the conversion
    ag_ins = _ag_ins
    ins_sizes = [ag_in.shape for ag_in in ag_ins]
    ins_split_sizes_bytes = [
        ag_in.numel() * out_dtype.itemsize
        for ag_in, out_dtype in zip(ag_ins, out_dtypes)
    ]
    bucket_dtype_size_bytes = dtype.itemsize
    ins_split_sizes = [
        _bytes // bucket_dtype_size_bytes for _bytes in ins_split_sizes_bytes
    ]
    ag_input_numel = sum(ins_split_sizes)

    # Convert out_dtypes to indices for custom_op
    # TODO: custom ops support list[dtype] input
    out_dtype_ints = [_ALL_DTYPES.index(dt) for dt in out_dtypes]

    # Pre-compute foreach groups for better foreach_copy_ performance
    foreach_group_indices = _compute_foreach_groups(ag_ins, out_dtypes)

    new_ag_out = torch.ops.bucketing._pre_bucket_all_gather(
        ag_ins,
        group_size,
        group_name,
        dtype,
        out_dtype_ints,
        rank,
        foreach_group_indices,
    )
    new_ag_in = new_ag_out.narrow(0, ag_input_numel * rank, ag_input_numel)
    wait_tensor = torch.ops.c10d_functional.wait_tensor(
        torch.ops._c10d_functional.all_gather_into_tensor_out.default(
            new_ag_in, group_size, group_name, out=new_ag_out
        )
    )
    new_ag_out_reshaped = wait_tensor.reshape(group_size, -1)
    outs_bucket_dtype = torch.split_with_sizes(
        new_ag_out_reshaped,
        ins_split_sizes,
        dim=1,
    )
    outs_reshaped = [
        o.view(out_dtype).reshape((shape[0] * group_size,) + shape[1:])
        for o, shape, out_dtype in zip(outs_bucket_dtype, ins_sizes, out_dtypes)
    ]
    return outs_reshaped

