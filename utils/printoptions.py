
def printoptions(**kwargs):
    r"""Context manager that temporarily changes the print options.  Accepted
    arguments are same as :func:`set_printoptions`."""
    old_kwargs = get_printoptions()
    set_printoptions(**kwargs)
    try:
        yield
    finally:
        set_printoptions(**old_kwargs)


def printoptions(*args, **kwargs):
    """Context manager for setting print options.

    Set print options for the scope of the `with` block, and restore the old
    options at the end. See `set_printoptions` for the full description of
    available options.

    Examples
    --------
    >>> import numpy as np

    >>> from numpy.testing import assert_equal
    >>> with np.printoptions(precision=2):
    ...     np.array([2.0]) / 3
    array([0.67])

    The `as`-clause of the `with`-statement gives the current print options:

    >>> with np.printoptions(precision=2) as opts:
    ...      assert_equal(opts, np.get_printoptions())

    See Also
    --------
    set_printoptions, get_printoptions

    Notes
    -----
    These print options apply only to NumPy ndarrays, not to scalars.

    **Concurrency note:** see :ref:`text_formatting_options`

    """
    token = _set_printoptions(*args, **kwargs)

    try:
        yield get_printoptions()
    finally:
        format_options.reset(token)


def printoptions(*args, **kwargs):
  """Alias of :func:`numpy.printoptions`.

  JAX arrays are printed via NumPy, so NumPy's `printoptions`
  configurations will apply to printed JAX arrays.

  See the :func:`numpy.set_printoptions` documentation for details
  on the available options and their meanings.
  """
  return np.printoptions(*args, **kwargs)

