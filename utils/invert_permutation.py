
def invert_permutation(permutation: Tensor | None) -> Tensor | None:
    """Returns the inverse of ``permutation``.

    This is useful for converting between sorted and unsorted indices in
    a :class:`~nn.utils.rnn.PackedSequence`.

    Args:
        permutation (Tensor, optional): a 1-D tensor of indices to invert
    """
    if permutation is None:
        return None
    output = torch.empty_like(permutation, memory_format=torch.legacy_contiguous_format)
    output.scatter_(
        0, permutation, torch.arange(0, permutation.numel(), device=permutation.device)
    )
    return output


def invert_permutation(i: Array) -> Array:
  """Helper function that inverts a permutation array."""
  return jnp.empty_like(i).at[i].set(jnp.arange(i.size, dtype=i.dtype))

