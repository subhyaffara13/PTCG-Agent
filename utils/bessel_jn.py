
def bessel_jn(z: ArrayLike, *, v: int, n_iter: int=50) -> Array:
  """Bessel function of the first kind of integer order and real argument.

  Reference:
  Shanjie Zhang and Jian-Ming Jin. Computation of special functions.
  Wiley-Interscience, 1996.

  Args:
    z: The sampling point(s) at which the Bessel function of the first kind are
      computed.
    v: The order (int) of the Bessel function.
    n_iter: The number of iterations required for updating the function
      values. As a rule of thumb, `n_iter` is the smallest nonnegative integer
      that satisfies the condition
      `int(0.5 * log10(6.28 + n_iter) - n_iter *  log10(1.36 + abs(z) / n_iter)) > 20`.
      Details in `BJNDD` (https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.f)

  Returns:
    An array of shape `(v+1, *z.shape)` containing the values of the Bessel
    function of orders 0, 1, ..., v. The return type matches the type of `z`.

  Raises:
    TypeError if `v` is not integer.
    ValueError if elements of array `z` are not float.
  """
  z = jnp.asarray(z)
  z, = promote_dtypes_inexact(z)
  z_dtype = lax.dtype(z)
  if dtypes.issubdtype(z_dtype, complex):
    raise ValueError("complex input not supported.")

  v = core.concrete_or_error(operator.index, v, 'Argument v of bessel_jn.')
  n_iter = core.concrete_or_error(int, n_iter, 'Argument n_iter of bessel_jn.')

  bessel_jn_fun = partial(_bessel_jn, v=v, n_iter=n_iter)
  for _ in range(z.ndim):
    bessel_jn_fun = vmap(bessel_jn_fun)
  return jnp.moveaxis(bessel_jn_fun(z), -1, 0)

