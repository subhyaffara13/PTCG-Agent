
def arctanh(x):
    """
    Compute the inverse hyperbolic tangent of `x`.

    Return the "principal value" (for a description of this, see
    `numpy.arctanh`) of ``arctanh(x)``. For real `x` such that
    ``abs(x) < 1``, this is a real number.  If `abs(x) > 1`, or if `x` is
    complex, the result is complex. Finally, `x = 1` returns``inf`` and
    ``x=-1`` returns ``-inf``.

    Parameters
    ----------
    x : array_like
       The value(s) whose arctanh is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The inverse hyperbolic tangent(s) of the `x` value(s). If `x` was
       a scalar so is `out`, otherwise an array is returned.


    See Also
    --------
    numpy.arctanh

    Notes
    -----
    For an arctanh() that returns ``NAN`` when real `x` is not in the
    interval ``(-1,1)``, use `numpy.arctanh` (this latter, however, does
    return +/-inf for ``x = +/-1``).

    Examples
    --------
    >>> import numpy as np
    >>> np.set_printoptions(precision=4)

    >>> np.emath.arctanh(0.5)
    0.5493061443340549

    >>> import warnings
    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter('ignore', RuntimeWarning)
    ...     np.emath.arctanh(np.eye(2))
    array([[inf,  0.],
           [ 0., inf]])
    >>> np.emath.arctanh([1j])
    array([0.+0.7854j])

    """
    x = _fix_real_abs_gt_1(x)
    return nx.arctanh(x)


def arctanh(x: ArrayLike, /) -> Array:
  r"""Calculate element-wise inverse of hyperbolic tangent of input.

  JAX implementation of :obj:`numpy.arctanh`.

  The inverse of hyperbolic tangent is defined by:

  .. math::

    arctanh(x) = \frac{1}{2} [\ln(1 + x) - \ln(1 - x)]

  Args:
    x: input array or scalar.

  Returns:
    An array of same shape as ``x`` containing the inverse of hyperbolic tangent
    of each element of ``x``, promoting to inexact dtype.

  Note:
    - ``jnp.arctanh`` returns ``nan`` for real-values outside the range ``[-1, 1]``.
    - ``jnp.arctanh`` follows the branch cut convention of :obj:`numpy.arctanh`
      for complex inputs.

  See also:
    - :func:`jax.numpy.tanh`: Computes the element-wise hyperbolic tangent of the
      input.
    - :func:`jax.numpy.arcsinh`: Computes the element-wise inverse of hyperbolic
      sine of the input.
    - :func:`jax.numpy.arccosh`: Computes the element-wise inverse of hyperbolic
      cosine of the input.

  Examples:
    >>> x = jnp.array([-2, -1, -0.5, 0, 0.5, 1, 2])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arctanh(x)
    Array([   nan,   -inf, -0.549,  0.   ,  0.549,    inf,    nan], dtype=float32)

    For complex-valued input:

    >>> x1 = jnp.array([-2+0j, 3+0j, 4-1j])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arctanh(x1)
    Array([-0.549+1.571j,  0.347+1.571j,  0.239-1.509j], dtype=complex64)
  """
  out = lax.atanh(*promote_args_inexact('arctanh', x))
  jnp_error._set_error_if_nan(out)
  return out

