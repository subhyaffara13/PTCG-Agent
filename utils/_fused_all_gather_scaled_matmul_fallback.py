
def _fused_all_gather_scaled_matmul_fallback(
    A_shard: torch.Tensor,
    Bs: list[torch.Tensor],
    A_scale: torch.Tensor,
    B_scales: list[torch.Tensor],
    gather_dim: int,
    group_name: c10d.GroupName,
    biases: list[torch.Tensor | None],
    result_scales: list[torch.Tensor | None],
    out_dtypes: list[torch.dtype | None],
    use_fast_accum: list[bool],
) -> tuple[torch.Tensor, list[torch.Tensor]]:
    out_dtypes = _maybe_convert_scalar_types_to_dtypes(out_dtypes)

    group_size = c10d._get_group_size_by_name(group_name)
    A = torch.ops._c10d_functional.all_gather_into_tensor(
        A_shard.contiguous(), group_size, group_name
    )
    A = torch.ops._c10d_functional.wait_tensor(A)
    A = A.view(group_size, *A_shard.shape).movedim(gather_dim + 1, 1).flatten(0, 1)

    scale_mode = _check_and_verify_fp8_all_gather_scale_mode(
        shard=A_shard, scale=A_scale, gather_dim=gather_dim, group_size=group_size
    )
    if scale_mode == _ScaleMode.ROW_WISE_SHARDED:
        A_scale_shard = A_scale
        A_scale = torch.ops._c10d_functional.all_gather_into_tensor(
            A_scale.contiguous(), group_size, group_name
        )
        A_scale = torch.ops._c10d_functional.wait_tensor(A_scale)
        A_scale = (
            A_scale.view(group_size, *A_scale_shard.shape)
            .movedim(gather_dim + 1, 1)
            .flatten(0, -2)
        )
    elif scale_mode == _ScaleMode.ROW_WISE_REPLICATED:
        A_scale = A_scale.movedim(gather_dim, 0).flatten(0, -2)
    else:
        if scale_mode != _ScaleMode.TENSOR_WISE:
            raise AssertionError

    def scaled_matmul(
        A: torch.Tensor,
        B: torch.Tensor,
        A_scale: torch.Tensor,
        B_scale: torch.Tensor,
        bias: torch.Tensor | None,
        result_scale: torch.Tensor | None,
        out_dtype: torch.dtype | None,
        use_fast_accum: bool,
    ) -> torch.Tensor:
        leading_dims = A.shape[:-1]
        res = torch.ops.aten._scaled_mm(
            A.flatten(0, -2),
            B,
            A_scale,
            B_scale,
            bias,
            result_scale,
            out_dtype=out_dtype,
            use_fast_accum=use_fast_accum,
        )
        return res.unflatten(0, leading_dims)

    return A.movedim(0, gather_dim), [
        scaled_matmul(
            A, B, A_scale, B_scale, bias, result_scale, out_dtype, fast_accum
        ).movedim(0, gather_dim)
        for B, B_scale, bias, result_scale, out_dtype, fast_accum in zip(
            Bs, B_scales, biases, result_scales, out_dtypes, use_fast_accum
        )
    ]

