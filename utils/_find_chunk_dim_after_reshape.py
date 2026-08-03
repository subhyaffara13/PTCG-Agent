import math


def _find_chunk_dim_after_reshape(
    old_shape: Sequence[int], new_shape: Sequence[int], chunk_dim: int
) -> int | None:
    """
    Find the equivalent chunk_dim position after a reshape by matching
    the prefix product (number of elements before the dimension) and
    the dimension size. Returns None if the chunk dimension is merged
    or split by the reshape, making it unsafe to propagate.

    Examples:
      [M, N] -> [M, N, 1], chunk_dim=0: returns 0 (trailing dim added)
      [M]    -> [M, 1],     chunk_dim=0: returns 0
      [M, N] -> [M1, M2, N] where M1*M2=M, chunk_dim=0: returns None (split)
      [M, N] -> [M*N],      chunk_dim=0: returns None (merged)
    """
    chunk_size = old_shape[chunk_dim]
    old_offset = math.prod(old_shape[:chunk_dim])
    new_offset = 1
    for new_dim in range(len(new_shape)):
        if new_offset == old_offset and new_shape[new_dim] == chunk_size:
            return new_dim
        new_offset *= new_shape[new_dim]
    return None

