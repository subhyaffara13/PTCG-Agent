
def check_error(res: int) -> None:
    r"""Raise an error if the result of a CUDA runtime API call is not success."""
    # pyrefly: ignore [missing-attribute]
    if res != _cudart.cudaError.success:
        raise CudaError(res)


def check_error(error: Error) -> None:
  """Raise an Exception if ``error`` represents a failure. Functionalized by :func:`~checkify`.

  The semantics of this function are equivalent to:

  >>> def check_error(err: Error) -> None:
  ...   err.throw()  # can raise ValueError

  But unlike that implementation, ``check_error`` can be functionalized using
  the :func:`~checkify` transformation.

  This function is similar to :func:`~check` but with a different signature: whereas
  :func:`~check` takes as arguments a boolean predicate and a new error message
  string, this function takes an ``Error`` value as argument. Both :func:`~check`
  and this function raise a Python Exception on failure (a side-effect), and
  thus cannot be staged out by :func:`~jax.jit`, :func:`~jax.pmap`,
  :func:`~jax.lax.scan`, etc. Both also can
  be functionalized by using :func:`~checkify`.

  But unlike :func:`~check`, this function is like a direct inverse of
  :func:`~checkify`:
  whereas :func:`~checkify` takes as input a function which
  can raise a Python
  Exception and produces a new function without that effect but which produces
  an ``Error`` value as output, this ``check_error`` function can accept an
  ``Error`` value as input and can produce the side-effect of raising an
  Exception. That is, while :func:`~checkify` goes from
  functionalizable Exception
  effect to error value, this ``check_error`` goes from error value to
  functionalizable Exception effect.

  ``check_error`` is useful when you want to turn checks represented by an
  ``Error`` value (produced by functionalizing ``checks`` via
  :func:`~checkify`) back into Python Exceptions.

  Args:
    error: Error to check.

  For example, you might want to functionalize part of your program through
  checkify, stage out your functionalized code through :func:`~jax.jit`, then
  re-inject your error value outside of the :func:`~jax.jit`:

  >>> import jax
  >>> from jax.experimental import checkify
  >>> def f(x):
  ...   checkify.check(x>0, "must be positive!")
  ...   return x
  >>> def with_inner_jit(x):
  ...   checked_f = checkify.checkify(f)
  ...   # a checkified function can be jitted
  ...   error, out = jax.jit(checked_f)(x)
  ...   checkify.check_error(error)
  ...   return out
  >>> _ = with_inner_jit(1)  # no failed check
  >>> with_inner_jit(-1)  # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
    ...
  jax._src.JaxRuntimeError: must be positive!
  >>> # can re-checkify
  >>> error, _ = checkify.checkify(with_inner_jit)(-1)
  """
  if not isinstance(error, Error):
    raise TypeError('check_error takes an Error as argument, '
                     f'got type {type(error)} instead.')
  _check_error(error, debug=False)

