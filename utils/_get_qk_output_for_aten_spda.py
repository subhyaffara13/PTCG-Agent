
def _get_qk_output_for_aten_spda(
    Q: torch.Tensor,
    K: torch.Tensor,
    current_q_num_heads: int,
    current_kv_num_heads: int,
    scale: float | None,
    qk_matmul_output_mode: int,
) -> torch.Tensor:
    """Get QK output tensor based on the specified mode."""
    if qk_matmul_output_mode == 0:
        return _compute_qk_output_for_mode_0(
            Q, K, current_q_num_heads, current_kv_num_heads, scale
        )
    else:
        # For other modes, return a zero tensor with correct shape
        return torch.zeros_like(torch.matmul(Q, K.transpose(-2, -1)))

