
def _prepare_patch_cross_attention_mask(
    patch_ids: torch.Tensor,
    num_patches: int,
    sequence_length: int,
    patches_as_queries: bool = False,
    cross_attn_k: int = 1,
    dtype: torch.dtype = torch.float32,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Prepare cross-attention mask for patch-based attention, following mllama's robust approach.

    This function creates masks that control which patches can attend to which other patches,
    with support for query/key role swapping and cross-attention multipliers.

    Args:
        patch_ids (torch.Tensor): Tensor of shape [batch_size, seq_len] containing patch ids.
        num_patches (int): Total number of patches.
        sequence_length (int): Length of the sequence.
        patches_as_queries (bool): If True, patches are used as queries, otherwise as keys.
        cross_attn_k (int): Cross-attention multiplier for repeating patches.
        dtype (torch.dtype): Data type for the output mask.

    Returns:
        Tuple[torch.Tensor, torch.Tensor]:
            - cross_attention_mask: 4D tensor [batch_size, 1, q_len, kv_len]
    """
    batch_size, seq_len = patch_ids.shape
    device = patch_ids.device

    # Determine query and key lengths based on configuration
    if patches_as_queries:
        q_len = num_patches * cross_attn_k
        kv_len = sequence_length
        # Create patch-to-sequence mapping
        q_patch_ids = (
            torch.arange(num_patches, device=device)
            .unsqueeze(0)
            .unsqueeze(-1)
            .expand(batch_size, num_patches, seq_len)
        )
        kv_patch_ids = patch_ids.unsqueeze(1).expand(batch_size, num_patches, seq_len)
    else:
        q_len = sequence_length
        kv_len = num_patches * cross_attn_k
        # Create sequence-to-patch mapping
        q_patch_ids = patch_ids.unsqueeze(-1).expand(batch_size, seq_len, num_patches)
        kv_patch_ids = (
            torch.arange(num_patches, device=device).unsqueeze(0).unsqueeze(0).expand(batch_size, seq_len, num_patches)
        )

    # Create base attention mask - boolean mask where True means "should attend"
    # Exact patch matching
    cross_attention_mask = q_patch_ids == kv_patch_ids

    # Handle cross_attn_k multiplier by repeating along appropriate dimension
    repeat_dim = 1 if patches_as_queries else -1
    cross_attention_mask = cross_attention_mask.repeat_interleave(cross_attn_k, dim=repeat_dim)

    # Validate dimensions
    expected_shape = (batch_size, q_len, kv_len)
    if cross_attention_mask.shape != expected_shape:
        raise ValueError(
            f"Cross attention mask shape {cross_attention_mask.shape} doesn't match expected {expected_shape}"
        )

    # Reshape so it can be used by attn module - add head dimension
    cross_attention_mask = cross_attention_mask.unsqueeze(1)  # [batch_size, 1, q_len, kv_len]

    # Invert the mask (following mllama pattern exactly)
    # True -> 0.0 (attend), False -> 1.0 (will become -inf)
    inverted_cross_attn_mask = 1.0 - cross_attention_mask.to(dtype)
    cross_attention_mask = inverted_cross_attn_mask.masked_fill(
        inverted_cross_attn_mask.to(torch.bool), torch.finfo(dtype).min
    )

    return cross_attention_mask


def _prepare_patch_cross_attention_mask(
    patch_ids: torch.Tensor,
    num_patches: int,
    sequence_length: int,
    patches_as_queries: bool = False,
    cross_attn_k: int = 1,
    dtype: torch.dtype = torch.float32,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Prepare cross-attention mask for patch-based attention, following mllama's robust approach.

    This function creates masks that control which patches can attend to which other patches,
    with support for query/key role swapping and cross-attention multipliers.

    Args:
        patch_ids (torch.Tensor): Tensor of shape [batch_size, seq_len] containing patch ids.
        num_patches (int): Total number of patches.
        sequence_length (int): Length of the sequence.
        patches_as_queries (bool): If True, patches are used as queries, otherwise as keys.
        cross_attn_k (int): Cross-attention multiplier for repeating patches.
        dtype (torch.dtype): Data type for the output mask.

    Returns:
        Tuple[torch.Tensor, torch.Tensor]:
            - cross_attention_mask: 4D tensor [batch_size, 1, q_len, kv_len]
    """
    batch_size, seq_len = patch_ids.shape
    device = patch_ids.device

    # Determine query and key lengths based on configuration
    if patches_as_queries:
        q_len = num_patches * cross_attn_k
        kv_len = sequence_length
        # Create patch-to-sequence mapping
        q_patch_ids = (
            torch.arange(num_patches, device=device)
            .unsqueeze(0)
            .unsqueeze(-1)
            .expand(batch_size, num_patches, seq_len)
        )
        kv_patch_ids = patch_ids.unsqueeze(1).expand(batch_size, num_patches, seq_len)
    else:
        q_len = sequence_length
        kv_len = num_patches * cross_attn_k
        # Create sequence-to-patch mapping
        q_patch_ids = patch_ids.unsqueeze(-1).expand(batch_size, seq_len, num_patches)
        kv_patch_ids = (
            torch.arange(num_patches, device=device).unsqueeze(0).unsqueeze(0).expand(batch_size, seq_len, num_patches)
        )

    # Create base attention mask - boolean mask where True means "should attend"
    # Exact patch matching
    cross_attention_mask = q_patch_ids == kv_patch_ids

    # Handle cross_attn_k multiplier by repeating along appropriate dimension
    repeat_dim = 1 if patches_as_queries else -1
    cross_attention_mask = cross_attention_mask.repeat_interleave(cross_attn_k, dim=repeat_dim)

    # Validate dimensions
    expected_shape = (batch_size, q_len, kv_len)
    if cross_attention_mask.shape != expected_shape:
        raise ValueError(
            f"Cross attention mask shape {cross_attention_mask.shape} doesn't match expected {expected_shape}"
        )

    # Reshape so it can be used by attn module - add head dimension
    cross_attention_mask = cross_attention_mask.unsqueeze(1)  # [batch_size, 1, q_len, kv_len]

    # Invert the mask (following mllama pattern exactly)
    # True -> 0.0 (attend), False -> 1.0 (will become -inf)
    inverted_cross_attn_mask = 1.0 - cross_attention_mask.to(dtype)
    cross_attention_mask = inverted_cross_attn_mask.masked_fill(
        inverted_cross_attn_mask.to(torch.bool), torch.finfo(dtype).min
    )

    return cross_attention_mask

