
def apply_rotary_pos_emb_2d_self_attn(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for self-attention.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)

    Returns:
        Rotated (q, k) tensors
    """
    # Apply RoPE to queries
    q_embed = q.float()  # force upscale to float32 as in the original implementation
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)

    # Apply RoPE to keys (same embeddings as queries for self-attention)
    k_embed = k.float()  # force upscale to float32 as in the original implementation
    k_embed = (k_embed * cos) + (rotate_pairwise(k_embed) * sin)

    return q_embed.type_as(q), k_embed.type_as(k)


def apply_rotary_pos_emb_2d_self_attn(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for self-attention.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)

    Returns:
        Rotated (q, k) tensors
    """
    # Apply RoPE to queries
    q_embed = q.float()  # force upscale to float32 as in the original implementation
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)

    # Apply RoPE to keys (same embeddings as queries for self-attention)
    k_embed = k.float()  # force upscale to float32 as in the original implementation
    k_embed = (k_embed * cos) + (rotate_pairwise(k_embed) * sin)

    return q_embed.type_as(q), k_embed.type_as(k)

