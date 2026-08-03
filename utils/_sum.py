import functools

def _sum() -> Accumulator:
  """An Accumulator that computes the sum of microbatched outputs."""
  return _lift(
      Accumulator(
          init=jnp.zeros_like,
          update=lambda carry, value, _: carry + value,
          finalize=lambda x: x,
          aggregate=functools.partial(jnp.sum, axis=0),
      )
  )


def _sum(a, axis=None, dtype=None, out=None, keepdims=False,
         initial=_NoValue, where=True):
    return umr_sum(a, axis, dtype, out, keepdims, initial, where)


def _sum(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
         out: None = None, keepdims: bool = False, initial: ArrayLike | None = None,
         where: ArrayLike | None = None, promote_integers: bool = True) -> Array:
  """Sum of the elements of the array over a given axis.

  Refer to :func:`jax.numpy.sum` for full documentation.
  """
  return reductions.sum(self, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        where=where, promote_integers=promote_integers)


def _sum(self, *args, **kwargs):
  """Sum array along axis."""
  return sparsify(lambda x: x.sum(*args, **kwargs))(self)

