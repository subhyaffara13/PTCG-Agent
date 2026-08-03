from typing import Any

def hessian_diag(
    loss: LossFn,
    params: Any,
    inputs: jax.Array,
    targets: jax.Array,
) -> jax.Array:
  """Computes the diagonal hessian of `loss` at (`inputs`, `targets`).

  .. deprecated: 0.2.7. This function will be removed in 0.2.9

  Args:
    loss: the loss function.
    params: model parameters.
    inputs: inputs at which `loss` is evaluated.
    targets: targets at which `loss` is evaluated.

  Returns:
    A DeviceArray corresponding to the product to the Hessian of `loss`
    evaluated at `(params, inputs, targets)`.
  """
  vs = jnp.eye(_ravel(params).size)
  comp = lambda v: jnp.vdot(v, _ravel(hvp(loss, v, params, inputs, targets)))
  return jax.vmap(comp)(vs)

