
def _average_ctc_loss(
    logprobs: jax.typing.ArrayLike,
    logprob_paddings: jax.typing.ArrayLike,
    labels: jax.typing.ArrayLike,
    label_paddings: jax.typing.ArrayLike,
) -> jax.Array:
  return jnp.average(
      _classification.ctc_loss(
          logprobs, logprob_paddings, labels, label_paddings
      )
  )

