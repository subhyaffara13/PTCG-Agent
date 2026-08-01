
def rolling_polynomial_hash(token_tensor, prime: int = 1000000007):
    """
    A polynomial rolling hash algorithm that converts sequences
    of tokens into hash values. The hash is computed as:
        hash = (token_0 * prime^0 + token_1 * prime^1 + ... + token_n * prime^n)

    The rolling hash allows the model to efficiently
    identify and encode recurring byte-level patterns in the input text.

    Args:
        token_tensor (torch.Tensor): [batch_size, seq_len, group_size] containing token IDs to hash
        prime (int): Prime number used as the base for the polynomial hash.

    Returns:
        torch.Tensor: Hash values of shape [batch_size, seq_len] where each value
                     represents the hash of the corresponding token group

    Example:
        >>> tokens = torch.tensor([[1, 2, 3], [4, 5, 6]])
        >>> hashes = rolling_polynomial_hash(tokens, prime=31)
        >>> # hash[0] = 1*31^0 + 2*31^1 + 3*31^2
        >>> # hash[1] = 4*31^0 + 5*31^1 + 6*31^2
    """
    prime_tensor = torch.tensor(prime, dtype=torch.int64, device=token_tensor.device)
    powers = torch.arange(token_tensor.shape[-1], device=token_tensor.device)
    prime_powers = prime_tensor**powers
    return torch.sum(token_tensor * prime_powers, dim=-1)


def rolling_polynomial_hash(token_tensor, prime: int = 1000000007):
    """
    A polynomial rolling hash algorithm that converts sequences
    of tokens into hash values. The hash is computed as:
        hash = (token_0 * prime^0 + token_1 * prime^1 + ... + token_n * prime^n)

    The rolling hash allows the model to efficiently
    identify and encode recurring byte-level patterns in the input text.

    Args:
        token_tensor (torch.Tensor): [batch_size, seq_len, group_size] containing token IDs to hash
        prime (int): Prime number used as the base for the polynomial hash.

    Returns:
        torch.Tensor: Hash values of shape [batch_size, seq_len] where each value
                     represents the hash of the corresponding token group

    Example:
        >>> tokens = torch.tensor([[1, 2, 3], [4, 5, 6]])
        >>> hashes = rolling_polynomial_hash(tokens, prime=31)
        >>> # hash[0] = 1*31^0 + 2*31^1 + 3*31^2
        >>> # hash[1] = 4*31^0 + 5*31^1 + 6*31^2
    """
    prime_tensor = torch.tensor(prime, dtype=torch.int64, device=token_tensor.device)
    powers = torch.arange(token_tensor.shape[-1], device=token_tensor.device)
    prime_powers = prime_tensor**powers
    return torch.sum(token_tensor * prime_powers, dim=-1)

