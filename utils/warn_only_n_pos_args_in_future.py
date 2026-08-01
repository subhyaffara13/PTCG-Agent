
def warn_only_n_pos_args_in_future(fun, n):
  """Warns if more than ``n`` positional arguments are passed to ``fun``.

  For instance:
  >>> @functools.partial(chex.warn_only_n_pos_args_in_future, n=1)
  ... def f(a, b, c=1):
  ...   return a + b + c

  Will raise a DeprecationWarning if ``f`` is called with more than one
  positional argument (e.g. both f(1, 2, 3) and f(1, 2, c=3) raise a warning).

  Args:
    fun: the function to wrap.
    n: the number of positional arguments to allow.

  Returns:
    A wrapped function that emits a warning if more than `n` positional
    arguments are passed.
  """

  @functools.wraps(fun)
  def wrapper(*args, **kwargs):
    if len(args) > n:
      warnings.warn(
          f'only the first {n} arguments can be passed positionally '
          'additional args will become keyword-only soon',
          DeprecationWarning,
          stacklevel=2
          )
    return fun(*args, **kwargs)

  return wrapper

