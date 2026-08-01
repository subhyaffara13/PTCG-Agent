
def apply_rotary_pos_emb_2d_cross_attn(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    cos_k: torch.Tensor,
    sin_k: torch.Tensor,
    num_k_exclude_rope: int = 0,
    repeat_freqs_k: int = 1,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for cross-attention.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)
        cos_k: Cosine position embedding for keys of shape (seq_len, head_dim)
        sin_k: Sine position embedding for keys of shape (seq_len, head_dim)
        num_k_exclude_rope: Number of tokens at end of k to exclude from RoPE (e.g., object pointer tokens)
        repeat_freqs_k: Frequency repetition for keys in cross-attention (e.g., for spatial memory tokens)

    Returns:
        Rotated (q, k) tensors
    """
    # Apply RoPE to queries (always straightforward)
    q_embed = q.float()
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)

    # Split keys: RoPE tokens and excluded tokens (e.g., object pointers)
    num_total_k_tokens = k.shape[-2]
    k_for_rope = k[..., : num_total_k_tokens - num_k_exclude_rope, :]
    k_excluded = k[..., num_total_k_tokens - num_k_exclude_rope :, :]

    # Early return if no keys need RoPE
    if k_for_rope.shape[-2] == 0:
        return q_embed.type_as(q), k_excluded

    batch_size, num_heads, k_seq_len, channels_per_head = k_for_rope.shape

    # Handle temporal/spatial token structure for memory
    # Keys have temporal + spatial structure, only spatial tokens get RoPE
    tokens_per_group = k_seq_len // repeat_freqs_k
    spatial_tokens = cos_k.shape[-2]
    temporal_tokens = tokens_per_group - spatial_tokens

    # Reshape and separate temporal/spatial tokens
    k_grouped = k_for_rope.view(batch_size, num_heads, repeat_freqs_k, tokens_per_group, channels_per_head)
    k_temporal = k_grouped[..., :temporal_tokens, :].reshape(batch_size, num_heads, -1, channels_per_head)
    k_spatial = k_grouped[..., temporal_tokens:, :].reshape(batch_size, num_heads, -1, channels_per_head)

    # Only apply RoPE to spatial tokens
    k_rope_input = k_spatial

    # Prepare position embeddings for repeated groups
    if repeat_freqs_k > 1:
        cos_k = cos_k.repeat(1, 1, repeat_freqs_k, 1)
        sin_k = sin_k.repeat(1, 1, repeat_freqs_k, 1)

    # Apply RoPE to spatial tokens
    k_spatial_embed = k_rope_input.float()
    k_spatial_embed = (k_spatial_embed * cos_k) + (rotate_pairwise(k_spatial_embed) * sin_k)

    # Reconstruct: temporal + spatial tokens back to original structure
    k_spatial_reshaped = k_spatial_embed.view(batch_size, num_heads, repeat_freqs_k, -1, channels_per_head)
    k_temporal_reshaped = k_temporal.view(batch_size, num_heads, repeat_freqs_k, -1, channels_per_head)
    k_final = torch.cat([k_temporal_reshaped, k_spatial_reshaped], dim=3)
    k_final = k_final.view(batch_size, num_heads, k_seq_len, channels_per_head)

    # Combine RoPE-processed keys with excluded tokens
    k_embed = torch.cat([k_final.type_as(k), k_excluded], dim=-2)
    return q_embed.type_as(q), k_embed


def apply_rotary_pos_emb_2d_cross_attn(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    cos_k: torch.Tensor,
    sin_k: torch.Tensor,
    num_k_exclude_rope: int = 0,
    repeat_freqs_k: int = 1,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Apply rotary position embedding to query and key tensors for cross-attention.

    Args:
        q: Query tensor of shape (..., seq_len, head_dim)
        k: Key tensor of shape (..., seq_len, head_dim)
        cos: Cosine position embedding of shape (seq_len, head_dim)
        sin: Sine position embedding of shape (seq_len, head_dim)
        cos_k: Cosine position embedding for keys of shape (seq_len, head_dim)
        sin_k: Sine position embedding for keys of shape (seq_len, head_dim)
        num_k_exclude_rope: Number of tokens at end of k to exclude from RoPE (e.g., object pointer tokens)
        repeat_freqs_k: Frequency repetition for keys in cross-attention (e.g., for spatial memory tokens)

    Returns:
        Rotated (q, k) tensors
    """
    # Apply RoPE to queries (always straightforward)
    q_embed = q.float()
    q_embed = (q_embed * cos) + (rotate_pairwise(q_embed) * sin)

    # Split keys: RoPE tokens and excluded tokens (e.g., object pointers)
    num_total_k_tokens = k.shape[-2]
    k_for_rope = k[..., : num_total_k_tokens - num_k_exclude_rope, :]
    k_excluded = k[..., num_total_k_tokens - num_k_exclude_rope :, :]

    # Early return if no keys need RoPE
    if k_for_rope.shape[-2] == 0:
        return q_embed.type_as(q), k_excluded

    batch_size, num_heads, k_seq_len, channels_per_head = k_for_rope.shape

    # Handle temporal/spatial token structure for memory
    # Keys have temporal + spatial structure, only spatial tokens get RoPE
    tokens_per_group = k_seq_len // repeat_freqs_k
    spatial_tokens = cos_k.shape[-2]
    temporal_tokens = tokens_per_group - spatial_tokens

    # Reshape and separate temporal/spatial tokens
    k_grouped = k_for_rope.view(batch_size, num_heads, repeat_freqs_k, tokens_per_group, channels_per_head)
    k_temporal = k_grouped[..., :temporal_tokens, :].reshape(batch_size, num_heads, -1, channels_per_head)
    k_spatial = k_grouped[..., temporal_tokens:, :].reshape(batch_size, num_heads, -1, channels_per_head)

    # Only apply RoPE to spatial tokens
    k_rope_input = k_spatial

    # Prepare position embeddings for repeated groups
    if repeat_freqs_k > 1:
        cos_k = cos_k.repeat(1, 1, repeat_freqs_k, 1)
        sin_k = sin_k.repeat(1, 1, repeat_freqs_k, 1)

    # Apply RoPE to spatial tokens
    k_spatial_embed = k_rope_input.float()
    k_spatial_embed = (k_spatial_embed * cos_k) + (rotate_pairwise(k_spatial_embed) * sin_k)

    # Reconstruct: temporal + spatial tokens back to original structure
    k_spatial_reshaped = k_spatial_embed.view(batch_size, num_heads, repeat_freqs_k, -1, channels_per_head)
    k_temporal_reshaped = k_temporal.view(batch_size, num_heads, repeat_freqs_k, -1, channels_per_head)
    k_final = torch.cat([k_temporal_reshaped, k_spatial_reshaped], dim=3)
    k_final = k_final.view(batch_size, num_heads, k_seq_len, channels_per_head)

    # Combine RoPE-processed keys with excluded tokens
    k_embed = torch.cat([k_final.type_as(k), k_excluded], dim=-2)
    return q_embed.type_as(q), k_embed

