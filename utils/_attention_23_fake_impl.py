
def _attention_23_fake_impl(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    attn_mask: torch.Tensor | None = None,
    past_key: torch.Tensor | None = None,
    past_value: torch.Tensor | None = None,
    *,
    is_causal: bool = False,
    kv_num_heads: int = 0,
    q_num_heads: int = 0,
    qk_matmul_output_mode: int = 0,
    scale: float | None = None,
    softcap: float = 0.0,
    softmax_precision: int | None = None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Fake implementation for Attention-23 for torch.compile purposes."""
    batch_size = Q.shape[0]

    # Handle 3D vs 4D input shapes
    if len(Q.shape) == 3:
        # 3D input: (batch_size, sequence_length, hidden_size)
        q_sequence_length = Q.shape[1]
        output_shape = Q.shape  # Same shape as Q for 3D output

        # For present_key and present_value, we need 4D shapes
        if past_key is not None:
            present_key_shape = (
                batch_size,
                kv_num_heads,
                past_key.shape[2] + K.shape[1],  # Combined sequence length
                K.shape[2] // kv_num_heads,  # head_size
            )
        else:
            present_key_shape = (
                batch_size,
                kv_num_heads,
                K.shape[1],  # sequence_length
                K.shape[2] // kv_num_heads,  # head_size
            )
        present_value_shape = present_key_shape  # Same shape as present_key

        # QK output shape for 3D input (reshaped to 4D internally)
        qk_output_shape = (
            batch_size,
            q_num_heads,
            q_sequence_length,
            present_key_shape[2],  # kv_sequence_length
        )
    else:
        # 4D input: (batch_size, num_heads, sequence_length, head_size)
        q_sequence_length = Q.shape[2]
        # Same shape as Q for 4D output
        output_shape = Q.shape  # type: ignore[assignment]

        # Handle past key/value concatenation
        if past_key is not None:
            present_key_shape = (
                K.shape[0],  # batch_size
                K.shape[1],  # num_heads
                past_key.shape[2] + K.shape[2],  # Combined sequence length
                K.shape[3],  # head_size
            )
        else:
            present_key_shape = K.shape  # type: ignore[assignment]
        present_value_shape = present_key_shape  # Same shape as present_key

        # QK output shape
        qk_output_shape = (
            Q.shape[0],  # batch_size
            Q.shape[1],  # q_num_heads
            Q.shape[2],  # q_sequence_length
            present_key_shape[2],  # kv_sequence_length
        )

    # Create fake tensors with correct shapes and dtypes
    output = torch.empty(output_shape, dtype=Q.dtype, device=Q.device)
    present_key = torch.empty(present_key_shape, dtype=K.dtype, device=K.device)
    present_value = torch.empty(present_value_shape, dtype=V.dtype, device=V.device)
    qk_output = torch.empty(qk_output_shape, dtype=Q.dtype, device=Q.device)

    return output, present_key, present_value, qk_output

