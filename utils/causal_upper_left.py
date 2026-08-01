
def causal_upper_left(*size) -> CausalBias:
    """
    Creates an upper-left triangular causal bias.

    This function generates a upper-left triangular matrix to represent causal attention bias with a
    diagonal offset set so that the inclusive values are aligned to the upper left corner of the matrix.
    This equivalent to the `is_causal=True` argument in `scaled_dot_product_attention`.

    The equivalent pytorch code for constructing this bias is:

    .. code-block:: python

        torch.tril(torch.ones(size, dtype=torch.bool))

    For instance, with `shape=(3,4)`, the materialized bias tensor will be:

    .. code-block:: text

        [[1, 0, 0, 0],
         [1, 1, 0, 0],
         [1, 1, 1, 0]]

    Args:
        size: The size of the bias matrix.

    Returns:
        CausalBias: The UPPER_LEFT triangular causal bias variant.
    """
    if len(size) != 2:
        raise AssertionError("causal_upper_left only supports 2D tensors")
    seq_len_q, seq_len_kv = size
    return CausalBias(CausalVariant.UPPER_LEFT, seq_len_q, seq_len_kv)

