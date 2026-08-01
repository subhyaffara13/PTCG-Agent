
def piecewise(x, condlist, funclist, *args, **kw):
    """
    Evaluate a piecewise-defined function.

    Given a set of conditions and corresponding functions, evaluate each
    function on the input data wherever its condition is true.

    Parameters
    ----------
    x : ndarray or scalar
        The input domain.
    condlist : list of bool arrays or bool scalars
        Each boolean array corresponds to a function in `funclist`.  Wherever
        `condlist[i]` is True, `funclist[i](x)` is used as the output value.

        Each boolean array in `condlist` selects a piece of `x`,
        and should therefore be of the same shape as `x`.

        The length of `condlist` must correspond to that of `funclist`.
        If one extra function is given, i.e. if
        ``len(funclist) == len(condlist) + 1``, then that extra function
        is the default value, used wherever all conditions are false.
    funclist : list of callables, f(x,*args,**kw), or scalars
        Each function is evaluated over `x` wherever its corresponding
        condition is True.  It should take a 1d array as input and give a 1d
        array or a scalar value as output.  If, instead of a callable,
        a scalar is provided then a constant function (``lambda x: scalar``) is
        assumed.
    args : tuple, optional
        Any further arguments given to `piecewise` are passed to the functions
        upon execution, i.e., if called ``piecewise(..., ..., 1, 'a')``, then
        each function is called as ``f(x, 1, 'a')``.
    kw : dict, optional
        Keyword arguments used in calling `piecewise` are passed to the
        functions upon execution, i.e., if called
        ``piecewise(..., ..., alpha=1)``, then each function is called as
        ``f(x, alpha=1)``.

    Returns
    -------
    out : ndarray
        The output is the same shape and type as x and is found by
        calling the functions in `funclist` on the appropriate portions of `x`,
        as defined by the boolean arrays in `condlist`.  Portions not covered
        by any condition have a default value of 0.


    See Also
    --------
    choose, select, where

    Notes
    -----
    This is similar to choose or select, except that functions are
    evaluated on elements of `x` that satisfy the corresponding condition from
    `condlist`.

    The result is::

            |--
            |funclist[0](x[condlist[0]])
      out = |funclist[1](x[condlist[1]])
            |...
            |funclist[n2](x[condlist[n2]])
            |--

    Examples
    --------
    >>> import numpy as np

    Define the signum function, which is -1 for ``x < 0`` and +1 for ``x >= 0``.

    >>> x = np.linspace(-2.5, 2.5, 6)
    >>> np.piecewise(x, [x < 0, x >= 0], [-1, 1])
    array([-1., -1., -1.,  1.,  1.,  1.])

    Define the absolute value, which is ``-x`` for ``x <0`` and ``x`` for
    ``x >= 0``.

    >>> np.piecewise(x, [x < 0, x >= 0], [lambda x: -x, lambda x: x])
    array([2.5,  1.5,  0.5,  0.5,  1.5,  2.5])

    Apply the same function to a scalar value.

    >>> y = -2
    >>> np.piecewise(y, [y < 0, y >= 0], [lambda x: -x, lambda x: x])
    array(2)

    """
    x = asanyarray(x)
    n2 = len(funclist)

    # undocumented: single condition is promoted to a list of one condition
    if isscalar(condlist) or (
            not isinstance(condlist[0], (list, ndarray)) and x.ndim != 0):
        condlist = [condlist]

    condlist = asarray(condlist, dtype=bool)
    n = len(condlist)

    if n == n2 - 1:  # compute the "otherwise" condition.
        condelse = ~np.any(condlist, axis=0, keepdims=True)
        condlist = np.concatenate([condlist, condelse], axis=0)
        n += 1
    elif n != n2:
        raise ValueError(
            f"with {n} condition(s), either {n} or {n + 1} functions are expected"
        )

    y = zeros_like(x)
    for cond, func in zip(condlist, funclist):
        if not isinstance(func, collections.abc.Callable):
            y[cond] = func
        else:
            vals = x[cond]
            if vals.size > 0:
                y[cond] = func(vals, *args, **kw)

    return y


def piecewise(x: ArrayLike, condlist: Array | Sequence[ArrayLike],
              funclist: list[ArrayLike | Callable[..., Array]],
              *args, **kw) -> Array:
  """Evaluate a function defined piecewise across the domain.

  JAX implementation of :func:`numpy.piecewise`, in terms of :func:`jax.lax.switch`.

  Note:
    Unlike :func:`numpy.piecewise`, :func:`jax.numpy.piecewise` requires functions
    in ``funclist`` to be traceable by JAX, as it is implemented via
    :func:`jax.lax.switch`.

  Args:
    x: array of input values.
    condlist: boolean array or sequence of boolean arrays corresponding to the
      functions in ``funclist``. If a sequence of arrays, the length of each
      array must match the length of ``x``
    funclist: list of arrays or functions; must either be the same length as
      ``condlist``, or have length ``len(condlist) + 1``, in which case the
      last entry is the default applied when none of the conditions are True.
      Alternatively, entries of ``funclist`` may be numerical values, in which
      case they indicate a constant function.
    args, kwargs: additional arguments are passed to each function in
      ``funclist``.

  Returns:
    An array which is the result of evaluating the functions on ``x`` at
    the specified conditions.

  See also:
    - :func:`jax.lax.switch`: choose between *N* functions based on an index.
    - :func:`jax.lax.cond`: choose between two functions based on a boolean condition.
    - :func:`jax.numpy.where`: choose between two results based on a boolean mask.
    - :func:`jax.lax.select`: choose between two results based on a boolean mask.
    - :func:`jax.lax.select_n`: choose between *N* results based on a boolean mask.

  Examples:
    Here's an example of a function which is zero for negative values, and linear
    for positive values:

    >>> x = jnp.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])

    >>> condlist = [x < 0, x >= 0]
    >>> funclist = [lambda x: 0 * x, lambda x: x]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([0, 0, 0, 0, 0, 1, 2, 3, 4], dtype=int32)

    ``funclist`` can also contain a simple scalar value for constant functions:

    >>> condlist = [x < 0, x >= 0]
    >>> funclist = [0, lambda x: x]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([0, 0, 0, 0, 0, 1, 2, 3, 4], dtype=int32)

    You can specify a default value by appending an extra condition to ``funclist``:

    >>> condlist = [x < -1, x > 1]
    >>> funclist = [lambda x: 1 + x, lambda x: x - 1, 0]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([-3, -2,  -1,  0,  0,  0,  1,  2, 3], dtype=int32)

    ``condlist`` may also be a simple array of scalar conditions, in which case
    the associated function applies to the whole range

    >>> condlist = jnp.array([False, True, False])
    >>> funclist = [lambda x: x * 0, lambda x: x * 10, lambda x: x * 100]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([-40, -30, -20, -10,   0,  10,  20,  30,  40], dtype=int32)
  """
  x_arr = util.ensure_arraylike("piecewise", x)
  nc, nf = len(condlist), len(funclist)
  if nf == nc + 1:
    funclist = funclist[-1:] + funclist[:-1]
  elif nf == nc:
    funclist = [0] + list(funclist)
  else:
    raise ValueError(f"with {nc} condition(s), either {nc} or {nc+1} functions are expected; got {nf}")
  consts = {i: c for i, c in enumerate(funclist) if not callable(c)}
  funcs = {i: f for i, f in enumerate(funclist) if callable(f)}
  return _piecewise(x_arr, asarray(condlist, dtype=bool), consts,
                    frozenset(funcs.items()),  # dict is not hashable.
                    *args, **kw)

