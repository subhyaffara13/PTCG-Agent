
def apply_rotary_pos_emb_2d(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    num_k_exclude_rope: int = 0,
    repeat_freqs_k: bool = False,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for vision models.
    Follows the standard transformers library pattern.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)
        repeat_freqs_k: Whether to repeat frequencies for keys (for cross-attention)

    Returns:
        Rotated (q, k) tensors
    """
    k_rot, k_pass = k[..., : k.shape[-2] - num_k_exclude_rope, :], k[..., k.shape[-2] - num_k_exclude_rope :, :]
    q_embed = q.float()  # force upscale to float32 as in the original implementation
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)
    if k_rot.shape[-2] == 0:
        # Handle case where keys might be empty due to dropout
        return q_embed.type_as(q), torch.cat([k_rot, k_pass], dim=-2)

    # Handle key tensor - may need to repeat frequencies if different sequence length
    if repeat_freqs_k and k_rot.shape[-2] != q.shape[-2]:
        # Repeat cos/sin to match key sequence length
        repeat_factor = k_rot.shape[-2] // q.shape[-2]
        cos_k = cos.repeat(1, 1, repeat_factor, 1)
        sin_k = sin.repeat(1, 1, repeat_factor, 1)
    else:
        cos_k = cos
        sin_k = sin

    # Apply rotary embedding to keys
    k_embed = k_rot.float()  # force upscale to float32 as in the original implementation
    k_embed = (k_embed * cos_k) + (rotate_pairwise(k_embed) * sin_k)
    # Concatenate back to full shape
    k_embed = torch.cat([k_embed.type_as(k), k_pass], dim=-2)
    return q_embed.type_as(q), k_embed


def apply_rotary_pos_emb_2d(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    num_k_exclude_rope: int = 0,
    repeat_freqs_k: bool = False,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for vision models.
    Follows the standard transformers library pattern.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)
        repeat_freqs_k: Whether to repeat frequencies for keys (for cross-attention)

    Returns:
        Rotated (q, k) tensors
    """
    k_rot, k_pass = k[..., : k.shape[-2] - num_k_exclude_rope, :], k[..., k.shape[-2] - num_k_exclude_rope :, :]
    q_embed = q.float()  # force upscale to float32 as in the original implementation
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)
    if k_rot.shape[-2] == 0:
        # Handle case where keys might be empty due to dropout
        return q_embed.type_as(q), torch.cat([k_rot, k_pass], dim=-2)

    # Handle key tensor - may need to repeat frequencies if different sequence length
    if repeat_freqs_k and k_rot.shape[-2] != q.shape[-2]:
        # Repeat cos/sin to match key sequence length
        repeat_factor = k_rot.shape[-2] // q.shape[-2]
        cos_k = cos.repeat(1, 1, repeat_factor, 1)
        sin_k = sin.repeat(1, 1, repeat_factor, 1)
    else:
        cos_k = cos
        sin_k = sin

    # Apply rotary embedding to keys
    k_embed = k_rot.float()  # force upscale to float32 as in the original implementation
    k_embed = (k_embed * cos_k) + (rotate_pairwise(k_embed) * sin_k)
    # Concatenate back to full shape
    k_embed = torch.cat([k_embed.type_as(k), k_pass], dim=-2)
    return q_embed.type_as(q), k_embed


def apply_rotary_pos_emb_2d(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for self-attention.

    Args:
        q: Query tensor of shape (batch_size, num_windows, seq_len, num_heads, head_dim)
        k: Key tensor of shape (batch_size, num_windows, seq_len, num_heads, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)

    Returns:
        Rotated (q, k) tensors
    """
    q_embed = q.float()
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)

    k_embed = k.float()
    k_embed = (k_embed * cos) + (rotate_pairwise(k_embed) * sin)

    return q_embed.type_as(q), k_embed.type_as(k)


def apply_rotary_pos_emb_2d(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    num_k_exclude_rope: int = 0,
    repeat_freqs_k: bool = False,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for vision models.
    Follows the standard transformers library pattern.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)
        repeat_freqs_k: Whether to repeat frequencies for keys (for cross-attention)

    Returns:
        Rotated (q, k) tensors
    """
    k_rot, k_pass = k[..., : k.shape[-2] - num_k_exclude_rope, :], k[..., k.shape[-2] - num_k_exclude_rope :, :]
    q_embed = q.float()  # force upscale to float32 as in the original implementation
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)
    if k_rot.shape[-2] == 0:
        # Handle case where keys might be empty due to dropout
        return q_embed.type_as(q), torch.cat([k_rot, k_pass], dim=-2)

    # Handle key tensor - may need to repeat frequencies if different sequence length
    if repeat_freqs_k and k_rot.shape[-2] != q.shape[-2]:
        # Repeat cos/sin to match key sequence length
        repeat_factor = k_rot.shape[-2] // q.shape[-2]
        cos_k = cos.repeat(1, 1, repeat_factor, 1)
        sin_k = sin.repeat(1, 1, repeat_factor, 1)
    else:
        cos_k = cos
        sin_k = sin

    # Apply rotary embedding to keys
    k_embed = k_rot.float()  # force upscale to float32 as in the original implementation
    k_embed = (k_embed * cos_k) + (rotate_pairwise(k_embed) * sin_k)
    # Concatenate back to full shape
    k_embed = torch.cat([k_embed.type_as(k), k_pass], dim=-2)
    return q_embed.type_as(q), k_embed

