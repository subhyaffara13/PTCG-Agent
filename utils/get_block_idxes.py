
def get_block_idxes(
    low_resolution_logit, num_blocks, approx_mode, initial_prior_first_n_blocks, initial_prior_diagonal_n_blocks
):
    """
    Compute the indices of the subset of components to be used in the approximation.
    """
    batch_size, total_blocks_per_row, _ = low_resolution_logit.shape

    if initial_prior_diagonal_n_blocks > 0:
        offset = initial_prior_diagonal_n_blocks // 2
        temp_mask = torch.ones(total_blocks_per_row, total_blocks_per_row, device=low_resolution_logit.device)
        diagonal_mask = torch.tril(torch.triu(temp_mask, diagonal=-offset), diagonal=offset)
        low_resolution_logit = low_resolution_logit + diagonal_mask[None, :, :] * 5e3

    if initial_prior_first_n_blocks > 0:
        low_resolution_logit[:, :initial_prior_first_n_blocks, :] = (
            low_resolution_logit[:, :initial_prior_first_n_blocks, :] + 5e3
        )
        low_resolution_logit[:, :, :initial_prior_first_n_blocks] = (
            low_resolution_logit[:, :, :initial_prior_first_n_blocks] + 5e3
        )

    top_k_vals = torch.topk(
        low_resolution_logit.reshape(batch_size, -1), num_blocks, dim=-1, largest=True, sorted=False
    )
    indices = top_k_vals.indices

    if approx_mode == "full":
        threshold = top_k_vals.values.min(dim=-1).values
        high_resolution_mask = (low_resolution_logit >= threshold[:, None, None]).float()
    elif approx_mode == "sparse":
        high_resolution_mask = None
    else:
        raise ValueError(f"{approx_mode} is not a valid approx_model value.")

    return indices, high_resolution_mask

