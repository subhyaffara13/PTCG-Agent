
def abs(a):
    return prims.abs(a)


def abs(g: jit_utils.GraphContext, self):
    return g.op("Abs", self)


def Abs(x):
    if isinstance(x, (int, float)):
        return interval(abs(x))
    elif isinstance(x, interval):
        if x.start < 0 and x.end > 0:
            return interval(0, max(abs(x.start), abs(x.end)), is_valid=x.is_valid)
        else:
            return interval(abs(x.start), abs(x.end))
    else:
        raise NotImplementedError


def abs(X, /):
    r"""Absolute value of a random variable.

    Parameters
    ----------
    X : `ContinuousDistribution`
        The random variable :math:`X`.

    Returns
    -------
    Y : `ContinuousDistribution`
        A random variable :math:`Y = |X|`.

    Examples
    --------
    Suppose we have a normally distributed random variable :math:`X`:

    >>> import numpy as np
    >>> from scipy import stats
    >>> X = stats.Normal()

    We wish to have a random variable :math:`Y` distributed according to
    the folded normal distribution; that is, a random variable :math:`|X|`.

    >>> Y = stats.abs(X)

    The PDF of the distribution in the left half plane is "folded" over to
    the right half plane. Because the normal PDF is symmetric, the resulting
    PDF is zero for negative arguments and doubled for positive arguments.

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(0, 5, 300)
    >>> ax = plt.gca()
    >>> Y.plot(x='x', y='pdf', t=('x', -1, 5), ax=ax)
    >>> plt.plot(x, 2 * X.pdf(x), '--')
    >>> plt.legend(('PDF of `Y`', 'Doubled PDF of `X`'))
    >>> plt.show()

    """
    return FoldedDistribution(X)


def abs(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return AbsOp(operand=operand, results=results, loc=loc, ip=ip).result


def abs(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return AbsOp(operand=operand, results=results, loc=loc, ip=ip).result


def abs(x: ArrayLike) -> Array:
  r"""Elementwise absolute value: :math:`|x|`.

  This function lowers directly to the `stablehlo.abs`_ operation.

  Args:
    x: Input array. Must have signed integer, floating, or complex dtype.

  Returns:
    An array of the same shape as ``x`` containing the elementwise absolute value.
    For complex valued input, :math:`a + ib`, ``abs(x)`` returns :math:`\sqrt{a^2+b^2}`.

  See also:
    - :func:`jax.numpy.abs`: a more flexible NumPy-style ``abs`` implementation.

  .. _stablehlo.abs: https://openxla.org/stablehlo/spec#abs
  """
  return abs_p.bind(x)


def abs(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.absolute`."""
  return absolute(x)

