
def promote_dtype(*args, dtype=None, inexact=True) -> list[Any]:
  """ "Promotes input arguments to a specified or inferred dtype.

  All args are cast to the same dtype. See ``canonicalize_dtype`` for how
  this dtype is determined.

  The behavior of promote_dtype is mostly a convinience wrapper around
  ``jax.numpy.promote_types``. The differences being that it automatically casts
  all input to the inferred dtypes, allows inference to be overridden by a
  forced dtype, and has an optional check to garantuee the resulting dtype is
  inexact.

  Args:
    *args: JAX array compatible values. None values are returned as is.
    dtype: Optional dtype override. If specified the arguments are cast to the
      specified dtype instead and dtype inference is disabled.
    inexact: When True, the output dtype must be a subdtype of `jnp.inexact`.
      Inexact dtypes are real or complex floating points. This is useful when
      you want to apply operations that don't work directly on integers like
      taking a mean for example.

  Returns:
    The arguments cast to arrays of the same dtype.
  """
  dtype = canonicalize_dtype(*args, dtype=dtype, inexact=inexact)
  return [jnp.asarray(x, dtype) if x is not None else None for x in args]


def promote_dtype(args: T, /, *, dtype=None, inexact=True) -> T:
  """ "Promotes input arguments to a specified or inferred dtype.

  All args are cast to the same dtype. See ``canonicalize_dtype`` for how
  this dtype is determined.

  The behavior of promote_dtype is mostly a convinience wrapper around
  ``jax.numpy.promote_types``. The differences being that it automatically casts
  all input to the inferred dtypes, allows inference to be overridden by a
  forced dtype, and has an optional check to garantuee the resulting dtype is
  inexact.

  Args:
    *args: JAX array compatible values. None values
      are returned as is.
    dtype: Optional dtype override. If specified the arguments are cast to
      the specified dtype instead and dtype inference is disabled.
    inexact: When True, the output dtype must be a subdtype
    of `jnp.inexact`. Inexact dtypes are real or complex floating points. This
    is useful when you want to apply operations that don't work directly on
    integers like taking a mean for example.
  Returns:
    The arguments cast to arrays of the same dtype.
  """
  dtype = canonicalize_dtype(*args, dtype=dtype, inexact=inexact)
  arrays = tuple(jnp.asarray(x, dtype) if x is not None else None for x in args)
  return arrays  # type: ignore[return-value]

