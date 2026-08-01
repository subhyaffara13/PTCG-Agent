
def _handle_row_wise_mask(gather_inp, padding_idx, weight, world_size, rank):
    """
    Mask the input for embedding look-up for IDs which are not stored
    on the current rank. This function also adjust the ``padding_idx``
    so that it is only used on the rank where the corresponding row is
    stored.

    Note that, with ``max_norm`` flag on, only weights of rows being
    looked up will be re-normed. So we need an extra row for masked ID
    so that it does not affect the final result and ``max_norm``.

    Args:
        gather_inp: tensor to be applied op on gathered from all ranks.
        padding_idx: If specified, the entries at padding_idx do
            not contribute to the gradient; therefore, the embedding
            vector at padding_idx is not updated during training,
            i.e. it remains as a fixed "pad".
            Note that the embedding vector at padding_idx is
            excluded from the reduction.
        weight: weight tensor of Embedding look-up table.
        world_size: number of ranks.
        rank: # of cuda process.

    Returns:
        lookup_input: Tensor of masked input.
        padding_idx: adjusted padding_idx.
        padding_row: The extra row we used during lookup so that
            looking up does not affect ``max_norm``.
    """
    (start_pos, chunk_size) = get_chunk_sharding_params(
        weight.size(0), world_size, weight._sharding_spec, rank
    )
    mask = (gather_inp < start_pos) | (gather_inp >= start_pos + chunk_size)
    lookup_input = gather_inp.clone() - start_pos
    lookup_input[mask] = chunk_size
    if (
        padding_idx is not None
        and padding_idx >= start_pos
        and padding_idx < (start_pos + chunk_size)
    ):
        padding_idx = padding_idx - start_pos
    else:
        padding_idx = None

    # When max_norm is set, it will only re-norm the row being looked up.
    padding_row = torch.zeros(
        1, weight.size(1), device=gather_inp.device, dtype=weight.dtype
    )
    return lookup_input, padding_idx, padding_row

