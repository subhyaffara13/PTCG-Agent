
def multiclass_sparsemax_loss(
    scores: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
) -> jax.Array:
  """Multiclass sparsemax loss.

  Args:
    scores: scores produced by the model.
    labels: ground-truth integer labels.

  Returns:
    loss values

  References:
    Martins et al, `From Softmax to Sparsemax: A Sparse Model of Attention and
    Multi-Label Classification <https://arxiv.org/abs/1602.02068>`, 2016.
  """
  return jax.vmap(_multiclass_sparsemax_loss)(scores, labels)

