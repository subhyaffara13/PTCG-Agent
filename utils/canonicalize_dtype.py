from typing import Any, Optional

def canonicalize_dtype(
    dtype: Optional[jax.typing.DTypeLike],
) -> Optional[jax.typing.DTypeLike]:
  """Canonicalise a dtype, skip if None."""
  if dtype is not None:
    return jax.dtypes.canonicalize_dtype(dtype)
  return dtype


def canonicalize_dtype(
    dtype: Any, allow_extended_dtype: Literal[False] = False
) -> DType:
  ...


def canonicalize_dtype(
    dtype: Any, allow_extended_dtype: bool = False
) -> DType | ExtendedDType:
  ...


def canonicalize_dtype(dtype: Any, allow_extended_dtype: bool = False) -> DType | ExtendedDType:
  """Convert from a dtype to a canonical dtype based on config.x64_enabled."""
  return _canonicalize_dtype(config.enable_x64.value, allow_extended_dtype, dtype)


def canonicalize_dtype(
  *args, dtype: Dtype | None = None, inexact: bool = True
) -> Dtype:
  """Canonicalize an optional dtype to the definitive dtype.

  If the ``dtype`` is None this function will infer the dtype. If it is not
  None it will be returned unmodified or an exceptions is raised if the dtype
  is invalid.
  from the input arguments using ``jnp.result_type``.

  Args:
    *args: JAX array compatible values. None values
      are ignored.
    dtype: Optional dtype override. If specified the arguments are cast to
      the specified dtype instead and dtype inference is disabled.
    inexact: When True, the output dtype must be a subdtype
    of `jnp.inexact`. Inexact dtypes are real or complex floating points. This
    is useful when you want to apply operations that don't work directly on
    integers like taking a mean for example.
  Returns:
    The dtype that *args should be cast to.
  """
  if dtype is None:
    args_filtered = [jnp.asarray(x) for x in args if x is not None]
    dtype = jnp.result_type(*args_filtered)
    if inexact and not jnp.issubdtype(dtype, jnp.inexact):
      dtype = jnp.promote_types(jnp.float32, dtype)
  if inexact and not jnp.issubdtype(dtype, jnp.inexact):
    raise ValueError(f'Dtype must be inexact: {dtype}')
  return dtype


def canonicalize_dtype(
  *args, dtype: Dtype | None = None, inexact: bool = True
) -> Dtype:
  """Canonicalize an optional dtype to the definitive dtype.

  If the ``dtype`` is None this function will infer the dtype. If it is not
  None it will be returned unmodified or an exceptions is raised if the dtype
  is invalid.
  from the input arguments using ``jnp.result_type``.

  Args:
    *args: JAX array compatible values. None values
      are ignored.
    dtype: Optional dtype override. If specified the arguments are cast to
      the specified dtype instead and dtype inference is disabled.
    inexact: When True, the output dtype must be a subdtype
    of `jnp.inexact`. Inexact dtypes are real or complex floating points. This
    is useful when you want to apply operations that don't work directly on
    integers like taking a mean for example.
  Returns:
    The dtype that *args should be cast to.
  """
  if dtype is None:
    args_filtered = [jnp.asarray(x) for x in args if x is not None]
    dtype = jnp.result_type(*args_filtered)
    if inexact and not jnp.issubdtype(dtype, jnp.inexact):
      dtype = jnp.promote_types(jnp.float32, dtype)
  if inexact and not jnp.issubdtype(dtype, jnp.inexact):
    raise ValueError(f'Dtype must be inexact: {dtype}')
  return dtype

