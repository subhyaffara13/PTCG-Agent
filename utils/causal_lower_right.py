
def causal_lower_right(*size) -> CausalBias:
    """
    Creates a lower-right triangular causal bias.

    This function generates a lower-right triangular matrix to represent causal attention bias with a
    diagonal offset set so that the inclusive values are aligned to the lower right corner of the matrix.

    The equivalent pytorch code for constructing this bias is:

    .. code-block:: python

        diagonal_offset = size[1] - size[0]
        torch.tril(
            torch.ones(size, dtype=torch.bool),
            diagonal=diagonal_offset,
        )

    For instance, with `shape=(3,4)`, the materialized bias tensor will be:

    .. code-block:: text

        [[1, 1, 0, 0],
         [1, 1, 1, 0],
         [1, 1, 1, 1]]

    Args:
        size: The size of the bias matrix.

    Returns:
        CausalBias: The LOWER_RIGHT triangular causal bias variant.
    """
    if len(size) != 2:
        raise AssertionError("causal_lower_right only supports 2D tensors")
    seq_len_q, seq_len_kv = size
    return CausalBias(CausalVariant.LOWER_RIGHT, seq_len_q, seq_len_kv)

