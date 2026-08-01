
def apply_multidimensional_rope(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    position_ids: torch.Tensor,
    unsqueeze_dim: int = 2,
) -> torch.Tensor:
    """Applies multidimensional RoPE to inputs.

    Args:
        x (`torch.Tensor`): The tensor to embed.
        cos (`torch.Tensor`): The cosine part of the rotary embedding.
        sin (`torch.Tensor`): The sine part of the rotary embedding.
        position_ids (`torch.Tensor`, *optional*):
            If position_ids.ndim + 2 == x.ndim, then this function passes through to `apply_rotary_pos_emb()`.
            Otherwise, position_ids is used to split the inputs, x, into multiple pieces, where each piece is fed to
            `apply_rotary_pos_emb()`, and then concatenated back together.
        unsqueeze_dim (`int`, *optional*, defaults to 1):
            The 'unsqueeze_dim' argument specifies the dimension along which to unsqueeze cos[position_ids] and
            sin[position_ids] so that they can be properly broadcasted to the dimensions of q and k. For example, note
            that cos[position_ids] and sin[position_ids] have the shape [batch_size, seq_len, head_dim]. Then, if q and
            k have the shape [batch_size, heads, seq_len, head_dim], then setting unsqueeze_dim=1 makes
            cos[position_ids] and sin[position_ids] broadcastable to the shapes of q and k. Similarly, if q and k have
            the shape [batch_size, seq_len, heads, head_dim], then set unsqueeze_dim=2.

    Returns:
      Tensor of shape [B, L, N, H] with RoPE applied.
    """
    ndim = position_ids.shape[-1]
    num_input_channels = x.shape[-1]
    num_rotated_channels_per_dim = 2 * (num_input_channels // (2 * ndim))

    if num_rotated_channels_per_dim <= 0:
        raise ValueError(
            "Invalid configuration: num_rotated_channels_per_dim must be > 0, got"
            f" {num_rotated_channels_per_dim} (num_input_channels={num_input_channels},"
            f" ndim={ndim})"
        )

    # Correctly split the input tensor into ndim parts
    split_sizes = [num_rotated_channels_per_dim] * ndim
    x_parts = torch.split(x, split_sizes, dim=-1)
    cos_parts = torch.split(cos, split_sizes, dim=-1)
    sin_parts = torch.split(sin, split_sizes, dim=-1)
    y_parts = [
        apply_rotary_pos_emb(
            x=x_parts[k],
            cos=cos_parts[k],
            sin=sin_parts[k],
            unsqueeze_dim=unsqueeze_dim,
        )
        for k in range(ndim)
    ]
    return torch.cat(y_parts, dim=-1)


def apply_multidimensional_rope(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    position_ids: torch.Tensor,
    unsqueeze_dim: int = 2,
) -> torch.Tensor:
    """Applies multidimensional RoPE to inputs.

    Args:
        x (`torch.Tensor`): The tensor to embed.
        cos (`torch.Tensor`): The cosine part of the rotary embedding.
        sin (`torch.Tensor`): The sine part of the rotary embedding.
        position_ids (`torch.Tensor`, *optional*):
            If position_ids.ndim + 2 == x.ndim, then this function passes through to `apply_rotary_pos_emb()`.
            Otherwise, position_ids is used to split the inputs, x, into multiple pieces, where each piece is fed to
            `apply_rotary_pos_emb()`, and then concatenated back together.
        unsqueeze_dim (`int`, *optional*, defaults to 1):
            The 'unsqueeze_dim' argument specifies the dimension along which to unsqueeze cos[position_ids] and
            sin[position_ids] so that they can be properly broadcasted to the dimensions of q and k. For example, note
            that cos[position_ids] and sin[position_ids] have the shape [batch_size, seq_len, head_dim]. Then, if q and
            k have the shape [batch_size, heads, seq_len, head_dim], then setting unsqueeze_dim=1 makes
            cos[position_ids] and sin[position_ids] broadcastable to the shapes of q and k. Similarly, if q and k have
            the shape [batch_size, seq_len, heads, head_dim], then set unsqueeze_dim=2.

    Returns:
      Tensor of shape [B, L, N, H] with RoPE applied.
    """
    ndim = position_ids.shape[-1]
    num_input_channels = x.shape[-1]
    num_rotated_channels_per_dim = 2 * (num_input_channels // (2 * ndim))

    if num_rotated_channels_per_dim <= 0:
        raise ValueError(
            "Invalid configuration: num_rotated_channels_per_dim must be > 0, got"
            f" {num_rotated_channels_per_dim} (num_input_channels={num_input_channels},"
            f" ndim={ndim})"
        )

    # Correctly split the input tensor into ndim parts
    split_sizes = [num_rotated_channels_per_dim] * ndim
    x_parts = torch.split(x, split_sizes, dim=-1)
    cos_parts = torch.split(cos, split_sizes, dim=-1)
    sin_parts = torch.split(sin, split_sizes, dim=-1)
    y_parts = [
        apply_rotary_pos_emb(
            x=x_parts[k],
            cos=cos_parts[k],
            sin=sin_parts[k],
            unsqueeze_dim=unsqueeze_dim,
        )
        for k in range(ndim)
    ]
    return torch.cat(y_parts, dim=-1)

