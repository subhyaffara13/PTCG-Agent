
def jet() -> None:
    """
    Set the colormap to 'jet'.

    This changes the default colormap as well as the colormap of the current
    image if there is one. See ``help(colormaps)`` for more information.
    """
    set_cmap("jet")


def jet(fun, primals, series, factorial_scaled=True, **_):
  r"""Taylor-mode higher-order automatic differentiation.

  Args:
    fun: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard Python container of arrays or scalars.
    primals: The primal values at which the Taylor approximation of ``fun`` should be
      evaluated. Should be either a tuple or a list of arguments,
      and its length should be equal to the number of positional parameters of
      ``fun``.
    series: Higher order Taylor-series-coefficients.
      Together, `primals` and `series` make up a truncated Taylor polynomial.
      Should be either a tuple or a list of tuples or lists,
      and its length dictates the degree of the truncated Taylor polynomial.
    factorial_scaled: If True, each term in both the input and output series is scaled
      by the factorial of its order, so that the input and output series is a
      Taylor series. This is the default behavior so that the n-th order term
      in the input and output series is the n-th order derivative of the function.
      If False, the input and output series are the non-factorial scaled Taylor
      coefficients (i.e., the constant coefficients for each term in the Taylor
      series).

  Returns:
    A ``(primals_out, series_out)`` pair, where ``primals_out`` is ``fun(*primals)``,
    and together, ``primals_out`` and ``series_out`` are a
    truncated Taylor polynomial of :math:`f(h(\cdot))`.
    The ``primals_out`` value has the same Python tree structure as ``primals``,
    and the ``series_out`` value the same Python tree structure as ``series``.

  For example:

  >>> import jax
  >>> import jax.numpy as np

  Consider the function :math:`h(z) = z^3`, :math:`x = 0.5`,
  and the first few Taylor coefficients
  :math:`h_0=x^3`, :math:`h_1=3x^2`, and :math:`h_2=6x`.
  Let :math:`f(y) = \sin(y)`.

  >>> h0, h1, h2 = 0.5**3., 3.*0.5**2., 6.*0.5
  >>> f, df, ddf = np.sin, np.cos, lambda *args: -np.sin(*args)

  :func:`jet` returns the Taylor coefficients of :math:`f(h(z)) = \sin(z^3)`
  according to Faà di Bruno's formula:

  >>> f0, (f1, f2) =  jet(f, (h0,), ((h1, h2),))
  >>> print(f0,  f(h0))
  0.12467473 0.12467473

  >>> print(f1, df(h0) * h1)
  0.74414825 0.74414825

  >>> print(f2, ddf(h0) * h1 ** 2 + df(h0) * h2)
  2.9064636 2.9064634
  """
  try:
    order, = set(map(len, series))
  except ValueError:
    msg = "jet terms have inconsistent lengths for different arguments"
    raise ValueError(msg) from None

  # TODO(mattjj): consider supporting pytree inputs
  for i, (x, terms) in enumerate(zip(primals, series)):
    treedef = tree_structure(x)
    if not treedef_is_leaf(treedef):
      raise ValueError(f"primal value at position {i} is not an array")
    for j, t in enumerate(terms):
      treedef = tree_structure(t)
      if not treedef_is_leaf(treedef):
        raise ValueError(f"term {j} for argument {i} is not an array")

  @lu.transformation_with_aux2
  def flatten_fun_output(f, store, *args):
    ans = f(*args)
    ans, tree = tree_flatten(ans)
    store.store(tree)
    return ans

  f, out_tree = flatten_fun_output(
      lu.wrap_init(fun,
                   debug_info=api_util.debug_info("jet", fun, primals, {})))
  if factorial_scaled:
    series = [[(term / fact(order + 1)) for order, term in enumerate(terms)]
      for terms in series]
  out_primals, out_terms = jet_fun(jet_subtrace(f), order).call_wrapped(primals, series)
  if factorial_scaled:
    out_terms = [[term * fact(order + 1) for order, term in enumerate(terms)]
      for terms in out_terms]
  return tree_unflatten(out_tree(), out_primals), tree_unflatten(out_tree(), out_terms)

