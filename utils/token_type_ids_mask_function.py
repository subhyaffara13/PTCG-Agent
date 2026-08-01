
def token_type_ids_mask_function(
    token_type_ids: torch.Tensor | None,
    image_group_ids: torch.Tensor | None,
) -> Callable | None:
    """
    This function adds the correct offsets to the `q_idx` and `kv_idx` as the torch API can only accept lengths,
    not start and end indices.
    """
    # Do not return an additional mask in this case
    if token_type_ids is None:
        return None

    def inner_mask(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
        seq_length = image_group_ids.shape[-1]

        # clamp indices because with static cache they can go beyond `image_group_ids.shape[-1]`
        q_idx_clamped = q_idx.clamp(max=seq_length - 1)
        kv_idx_clamped = kv_idx.clamp(max=seq_length - 1)

        # Unmask if the q and kv come from same group which is not -1 (i.e. non-text)
        q_group = image_group_ids[batch_idx, q_idx_clamped]
        kv_group = image_group_ids[batch_idx, kv_idx_clamped]
        q_group = torch.where(q_idx < seq_length, q_group, -1)
        kv_group = torch.where(kv_idx < seq_length, kv_group, -1)
        return (q_group == kv_group) & (q_group >= 0)

    return inner_mask

