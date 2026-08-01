
def kl_divergence(p: Distribution, q: Distribution) -> Tensor:
    r"""
    Compute Kullback-Leibler divergence :math:`KL(p \| q)` between two distributions.

    .. math::

        KL(p \| q) = \int p(x) \log\frac {p(x)} {q(x)} \,dx

    Args:
        p (Distribution): A :class:`~torch.distributions.Distribution` object.
        q (Distribution): A :class:`~torch.distributions.Distribution` object.

    Returns:
        Tensor: A batch of KL divergences of shape `batch_shape`.

    Raises:
        NotImplementedError: If the distribution types have not been registered via
            :meth:`register_kl`.
    """
    try:
        fun = _KL_MEMOIZE[type(p), type(q)]
    except KeyError:
        fun = _dispatch_kl(type(p), type(q))
        _KL_MEMOIZE[type(p), type(q)] = fun
    if fun is NotImplemented:
        raise NotImplementedError(
            f"No KL(p || q) is implemented for p type {p.__class__.__name__} and q type {q.__class__.__name__}"
        )
    return fun(p, q)


def kl_divergence(
    log_predictions: jax.typing.ArrayLike,
    targets: jax.typing.ArrayLike,
    axis: Union[int, tuple[int, ...], None] = -1,
    where: Union[jax.typing.ArrayLike, None] = None,
) -> jax.Array:
  """Computes the Kullback-Leibler divergence (relative entropy) loss.

  Measures the information gain achieved if target probability distribution
  would be used instead of predicted probability distribution.

  Args:
    log_predictions: Probabilities of predicted distribution with shape [...,
      dim]. Expected to be in the log-space to avoid underflow.
    targets: Probabilities of target distribution with shape [..., dim].
      Expected to be strictly positive.
    axis: Axis or axes along which to compute.
    where: Elements to include in the computation.

  Returns:
    Kullback-Leibler divergence of predicted distribution from target
    distribution with shape [...].

  References:
    Kullback and Leibler, `On Information and Sufficiency
    <https://www.jstor.org/stable/2236703>`_, 1951

  .. versionchanged:: 0.2.4
    Added ``axis`` and ``where`` arguments.
  """
  utils.check_subdtype(log_predictions, jnp.floating)
  utils.check_subdtype(targets, jnp.floating)
  loss = targets * (
      jnp.where(targets == 0, 0, jnp.log(targets)) - log_predictions
  )
  return jnp.sum(loss, axis=axis, where=where)

