from typing import Callable, Optional

def _safe_reduce(
    a: jax.typing.ArrayLike,
    where: Optional[jax.typing.ArrayLike] = None,
    reduce_fn: Optional[Callable[..., jax.typing.ArrayLike]] = None,
) -> jax.Array:
  """Reduces the values of given array while preventing NaN in the output.

  For :func:`jax.numpy.mean` reduction, this additionally prevents ``NaN`` in
  the output if all elements are masked. This can happen with pairwise losses
  where there are no valid pairs because all labels are the same. In this
  situation, 0 is returned instead.

  When there is no ``reduce_fn``, this will set elements of ``a`` to 0 according
  to the ``where`` mask.

  Args:
    a: The :class:`jax.Array` to reduce.
    where: An optional :class:`jax.Array` indicating which elements to include
      in the reduction.
    reduce_fn: The function used to reduce. If None, no reduction is performed.

  Returns:
    The result of reducing the values of ``a`` using given ``reduce_fn``.
  """
  # Reduce values if there is a reduce_fn, otherwise keep the values as-is.
  output = reduce_fn(a, where=where) if reduce_fn is not None else a

  if reduce_fn is jnp.mean:
    # For mean reduction, we have to check whether the input contains any NaN
    # values, to ensure that masked mean reduction does not hide them (see
    # below).
    is_input_valid = jnp.logical_not(jnp.any(jnp.isnan(a)))

    # The standard jnp.mean implementation returns NaN if `where` is False
    # everywhere. This can happen in our case, e.g. pairwise losses with no
    # valid pairs. Instead, we prefer that the loss returns 0 in these cases.
    # Note that this only hides those NaN values if the input did not contain
    # any NaN values. Otherwise it just returns the output as-is.
    output = jnp.where(jnp.isnan(output) & is_input_valid, 0.0, output)

  if reduce_fn is None and where is not None:
    # When there is no reduce_fn (i.e. we are returning an unreduced
    # loss/metric), set the values of `a` to 0 for invalid (masked) items.
    # This makes sure that manual sum reduction on an unreduced loss works as
    # expected:
    # `jnp.sum(loss_fn(reduce_fn=None)) == loss_fn(reduce_fn=jnp.sum)`
    output = jnp.where(where, output, 0.0)

  return output  # pytype: disable=bad-return-type  # jax-arraylike

