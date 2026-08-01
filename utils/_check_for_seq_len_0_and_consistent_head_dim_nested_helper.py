
def _check_for_seq_len_0_and_consistent_head_dim_nested_helper(
    param: torch.Tensor, param_name: str, debug=False
) -> bool:
    if not isinstance(param, NestedTensor):
        raise AssertionError("param should be a jagged NT")

    if param._ragged_idx == 1:
        # num_head_dims is ragged
        if debug:
            log.warning(
                "Fused kernels do not support ragged num_head_dims, %s has a ragged num_heads.",
                param_name,
            )
        return False

    # This is being called inside sdp with shape [batch, heads, {seq_len}, dim]
    if param._get_min_seqlen() == 0:
        if debug:
            log.warning(
                "Fused kernels do not support seq_len == 0, %s has a seq len of 0.",
                param_name,
            )
        return False

    return True

