
def debug_check(pred: Bool, msg: str, *fmt_args, **fmt_kwargs) -> None:
  """Check a predicate when running under checkify, otherwise is a no-op.

  A `debug_check` will only be run if it is transformed by :func:`~checkify`,
  otherwise the check will be dropped.

  Args:
    pred: if False, a FailedCheckError error is added.
    msg: error message if error is added.
    fmt_args, fmt_kwargs: Positional and keyword formatting arguments for
      `msg`, eg.:
      ``debug_check(.., "check failed on values {} and {named}", x, named=y)``
      Note that these arguments can be traced values allowing you to add
      run-time values to the error message.
      Note that tracking these run-time arrays will increase your memory usage,
      even if no error happens.

  For example:

    >>> import jax
    >>> import jax.numpy as jnp
    >>> from jax.experimental import checkify
    >>> def f(x):
    ...   checkify.debug_check(x!=0, "cannot be zero!")
    ...   return x
    >>> _ = f(0)  # running without checkify means no debug_check is run.
    >>> checked_f = checkify.checkify(f)
    >>> err, out = jax.jit(checked_f)(0)  # running with checkify runs debug_check.
    >>> err.throw()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    jax._src.checkify.JaxRuntimeError: cannot be zero!

  """
  _check(pred, msg, True, *fmt_args, **fmt_kwargs)


def debug_check(condition, message):
  """Check the condition if
  :func:`~jax.experimental.pallas.enable_debug_checks` is set, otherwise
  do nothing.
  """
  return checkify.debug_check(condition, message)

