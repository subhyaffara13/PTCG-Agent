
def byte_group_hash_function(
    token_ids: torch.Tensor, group_size: int = 2, prime: int = 1000000007, max_hash: int = 30000
):
    """Hash token groups and map to range [0, max_hash]."""
    with torch.no_grad():
        batch_size, seq_len = token_ids.shape
        # Add padding for sliding window
        padding = torch.zeros(batch_size, group_size - 1, dtype=torch.int64, device=token_ids.device)
        padded_tokens = torch.cat([padding, token_ids], dim=1)

        # Create sliding windows and compute hashes
        windows = padded_tokens.unfold(1, group_size, 1)
        hashes = rolling_polynomial_hash(windows, prime)
        hash_values = hashes % max_hash

    return hash_values


def byte_group_hash_function(
    token_ids: torch.Tensor, group_size: int = 2, prime: int = 1000000007, max_hash: int = 30000
):
    """Hash token groups and map to range [0, max_hash]."""
    with torch.no_grad():
        batch_size, seq_len = token_ids.shape
        # Add padding for sliding window
        padding = torch.zeros(batch_size, group_size - 1, dtype=torch.int64, device=token_ids.device)
        padded_tokens = torch.cat([padding, token_ids], dim=1)

        # Create sliding windows and compute hashes
        windows = padded_tokens.unfold(1, group_size, 1)
        hashes = rolling_polynomial_hash(windows, prime)
        hash_values = hashes % max_hash

    return hash_values

