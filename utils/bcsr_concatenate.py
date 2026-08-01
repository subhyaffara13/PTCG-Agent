
def bcsr_concatenate(operands: Sequence[BCSR], *, dimension: int) -> BCSR:
  """Sparse implementation of :func:`jax.lax.concatenate`

  Args:
    operands : Sequence of BCSR arrays to concatenate. The arrays must have equal
      shapes, except in the `dimension` axis. Additionally, the arrays must have
      have equivalent batch, sparse, and dense dimensions.
    dimension : Positive integer specifying the dimension along which to concatenate
      the arrays. The dimension must be among batch or sparse dimensions of the input;
      concatenation along dense dimensions is not supported.

  Returns:
    A BCSR array containing the concatenation of the inputs.
  """
  return BCSR.from_bcoo(
    bcoo.bcoo_concatenate([mat.to_bcoo() for mat in operands], dimension=dimension))

