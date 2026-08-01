
def cosine_similarity(g: jit_utils.GraphContext, x1, x2, dim, eps):
    cross = symbolic_helper._reducesum_helper(
        g, mul(g, x1, x2), axes_i=[dim], keepdims_i=0
    )
    x1_l2 = symbolic_helper._reducesum_helper(
        g, mul(g, x1, x1), axes_i=[dim], keepdims_i=0
    )
    x2_l2 = symbolic_helper._reducesum_helper(
        g, mul(g, x2, x2), axes_i=[dim], keepdims_i=0
    )
    # pyrefly: ignore [no-matching-overload]
    div_tens = max(
        g, sqrt(g, mul(g, x1_l2, x2_l2)), g.op("Constant", value_t=torch.tensor([eps]))
    )
    return div(g, cross, div_tens)


def cosine_similarity(
    predictions: jax.typing.ArrayLike,
    targets: jax.typing.ArrayLike,
    *,
    epsilon: jax.typing.ArrayLike = 0.0,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  r"""Computes the cosine similarity between targets and predictions.

  The cosine **similarity** is a measure of similarity between vectors defined
  as the cosine of the angle between them, which is also the inner product of
  those vectors normalized to have unit norm.

  Args:
    predictions: The predicted vectors, with shape `[..., dim]`.
    targets: Ground truth target vectors, with shape `[..., dim]`.
    epsilon: minimum norm for terms in the denominator of the cosine similarity.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation.

  Returns:
    cosine similarity measures, with shape `[...]`.

  References:
    `Cosine similarity <https://en.wikipedia.org/wiki/Cosine_similarity>`_,
    Wikipedia.

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(predictions, jnp.floating)
  utils.check_subdtype(targets, jnp.floating)
  a = predictions
  b = targets

  # dot = (a * b).sum(axis=axis, where=where)
  # a_norm2 = jnp.square(a).sum(axis=axis, where=where)
  # b_norm2 = jnp.square(b).sum(axis=axis, where=where)
  # return dot / jnp.sqrt((a_norm2 * b_norm2))

  a_norm2 = jnp.square(a).sum(axis=axis, where=where, keepdims=True)
  b_norm2 = jnp.square(b).sum(axis=axis, where=where, keepdims=True)
  a_norm = jnp.sqrt(a_norm2.clip(epsilon))
  b_norm = jnp.sqrt(b_norm2.clip(epsilon))
  a_unit = a / a_norm
  b_unit = b / b_norm
  return (a_unit * b_unit).sum(axis=axis, where=where)

