
def reduce_scatter_merge_fn_to_trace_custom_ops(
    rs_ins: list[torch.Tensor],
    group_size: int,
    group_name: str,
    reduce_op: str,
    reduce_dtype: torch.dtype,  # type: ignore[name-defined]
    device: torch.device,  # type: ignore[name-defined]
) -> list[torch.Tensor]:  # type: ignore[no-untyped-def]
    new_out_sizes = [(x.shape[0] // group_size,) + x.shape[1:] for x in rs_ins]
    new_out_numels = [x.numel() // group_size for x in rs_ins]

    new_rs_in = torch.ops.bucketing._pre_bucket_reduce_scatter(rs_ins, group_size)

    # TODO - either use torch.cat or make sure inductor foreach codegen
    # fires more reliably
    new_rs_out = torch.ops.c10d_functional.wait_tensor(
        torch.ops._c10d_functional.reduce_scatter_tensor.default(
            new_rs_in, reduce_op, group_size, group_name
        )
    )
    new_out_flat = new_rs_out.split(new_out_numels, 0)
    new_outs = [x.view(s) for x, s in zip(new_out_flat, new_out_sizes)]
    return new_outs

