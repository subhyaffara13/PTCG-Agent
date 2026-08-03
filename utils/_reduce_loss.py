from typing import Optional

def _reduce_loss(
    loss: jax.Array, reduction: str, axis: Optional[int] = None
) -> jax.Array:
  if reduction == "mean":
    return jnp.mean(loss, axis=axis)
  elif reduction == "sum":
    return jnp.sum(loss, axis=axis)
  elif reduction == "none":
    return loss
  else:
    raise ValueError(f"Unsupported reduction: {reduction}")

