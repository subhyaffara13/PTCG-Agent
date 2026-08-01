
def isnan(x):
    if is_integer_type(x):
        return full_like(x, False, dtype=torch.bool)
    fn = ops_wrapper("isnan")
    return make_pointwise(fn, override_return_dtype=torch.bool)(x)


def isnan(a: TensorLikeType) -> TensorLikeType:
    return prims.ne(a, a)


def isnan(g: jit_utils.GraphContext, input):
    output = g.op("IsNaN", input)
    return output


def isnan(x):
  """Checks for NaN's in nested objects."""
  if isinstance(x, float):
    return np.isnan(x)
  elif isinstance(x, int):
    return np.isnan(x)
  elif isinstance(x, np.ndarray):
    return np.any(np.isnan(x))
  elif isinstance(x, list):
    return np.any([isnan(xi) for xi in x])
  elif isinstance(x, tuple):
    return np.any([isnan(xi) for xi in x])
  elif isinstance(x, dict):
    return np.any([isnan(xi) for xi in x.values()])
  else:
    typ = repr(type(x))
    err_string = 'type(x)={:s} not recognized when checking for NaN'.format(typ)
    raise NotImplementedError(err_string)


def isnan(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IsNaNOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def isnan(x: ArrayLike, /) -> Array:
  """Returns a boolean array indicating whether each element of input is ``NaN``.

  JAX implementation of :obj:`numpy.isnan`.

  Args:
    x: input array or scalar.

  Returns:
    A boolean array of same shape as ``x`` containing ``True`` where ``x`` is
    not a number (i.e. ``NaN``) and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.isfinite`: Returns a boolean array indicating whether each
      element of input is finite.
    - :func:`jax.numpy.isinf`: Returns a boolean array indicating whether each
      element of input is either positive or negative infinity.
    - :func:`jax.numpy.isposinf`: Returns a boolean array indicating whether each
      element of input is positive infinity.
    - :func:`jax.numpy.isneginf`: Returns a boolean array indicating whether each
      element of input is negative infinity.

  Examples:
    >>> jnp.isnan(6)
    Array(False, dtype=bool, weak_type=True)
    >>> x = jnp.array([2, 1+4j, jnp.inf, jnp.nan])
    >>> jnp.isnan(x)
    Array([False, False, False,  True], dtype=bool)
  """
  x = ensure_arraylike("isnan", x)
  return lax.ne(x, x)

