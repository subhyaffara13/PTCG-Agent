
def _check_and_verify_fp8_all_gather_scale_mode(
    shard: torch.Tensor, scale: torch.Tensor | None, gather_dim: int, group_size: int
) -> _ScaleMode:
    full_shape = list(shard.shape)
    full_shape[gather_dim] *= group_size

    if scale is None:
        return _ScaleMode.UNSCALED
    elif scale.shape[:-1] == shard.shape[:-1] and scale.shape[-1] == 1:
        # Row-wise scaling
        #
        # NOTE: when the last dim of both A_shard and A_scale is one, we can't
        # tell if A_scale is replicated tensor-wise scale or sharded row-wise
        # scale. Treating it as row-wise scaling for safety.
        return _ScaleMode.ROW_WISE_SHARDED
    elif scale.numel() == 1:
        return _ScaleMode.TENSOR_WISE
    elif list(scale.shape[:-1]) == full_shape[:-1]:
        return _ScaleMode.ROW_WISE_REPLICATED
    else:
        raise ValueError(
            "Invalid scale shape for fp8 all-gather "
            f"(shard shape: {shard.shape}, scale shape: {scale.shape})"
        )

