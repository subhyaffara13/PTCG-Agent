
def _extract_fns_kwargs(
    fns: tuple[Callable[..., Any], ...],
    kwargs: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
  """Split ``kwargs`` into sub_kwargs to be fed to each function in ``fns``.

  Given a dictionary of arguments ``kwargs`` and a list of functions
  ``fns = (fn_1, ..., fn_n)``, this utility splits the ``kwargs`` in several
  dictionaries ``(fn_1_kwargs, ..., fn_n_kwargs), remaining_kwargs``. Each
  dictionary ``fn_i_kwargs`` correspond to a subset of ``{key: values}`` pairs
  from ``kwargs`` such that ``key`` is one possible argument of the function
  ``fn_i``. The ``remaining_kwargs`` argument consist in all pairs
  ``{key: values}`` from ``kwargs`` whose ``key`` does not match any argument
  of any of the functions ``fns``.

  Args:
    fns: tuple of functions to feed kwargs to.
    kwargs: dictionary of keyword variables to be fed to funs.

  Returns:
    (fn_1_kwargs, ..., fn_n_kwargs)
      Keyword arguments for each function taken from kwargs.
    remaining_kwargs
      Keyword arguments present in kwargs but not in any of the input functions.

  Examples:
    >>> def fn1(a, b): return a+b
    >>> def fn2(c, d): return c+d
    >>> kwargs = {'b':1., 'd':2., 'e':3.}
    >>> fns_kwargs, remaining_kwargs = _extract_fns_kwargs((fn1, fn2), kwargs)
    >>> print(fns_kwargs)
    [{'b': 1.0}, {'d': 2.0}]
    >>> print(remaining_kwargs)
    {'e': 3.0}
    >>> # Possible usage
    >>> def super_fn(a, c, **kwargs):
    ...  (fn1_kwargs, fn2_kwargs), _ = _extract_fns_kwargs((fn1, fn2), kwargs)
    ...  return fn1(a, **fn1_kwargs) + fn2(c, **fn2_kwargs)
    >>> print(super_fn(1., 2., b=3., d=4.))
    10.0
  """
  fns_arg_names = [list(inspect.signature(fn).parameters.keys()) for fn in fns]
  fns_kwargs = [
      {k: v for k, v in kwargs.items() if k in fn_arg_names}
      for fn_arg_names in fns_arg_names
  ]
  all_possible_arg_names = functools.reduce(operator.add, fns_arg_names)
  remaining_keys = [k for k in kwargs.keys() if k not in all_possible_arg_names]
  remaining_kwargs = {k: v for k, v in kwargs.items() if k in remaining_keys}
  return fns_kwargs, remaining_kwargs

