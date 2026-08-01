
def _div(mul_f, c1, c2):
    """
    Helper function used to implement the ``<type>div`` functions.

    Implementation uses repeated subtraction of c2 multiplied by the nth basis.
    For some polynomial types, a more efficient approach may be possible.

    Parameters
    ----------
    mul_f : function(array_like, array_like) -> array_like
        The ``<type>mul`` function, such as ``polymul``
    c1, c2
        See the ``<type>div`` functions for more detail
    """
    # c1, c2 are trimmed copies
    [c1, c2] = as_series([c1, c2])
    if c2[-1] == 0:
        raise ZeroDivisionError  # FIXME: add message with details to exception

    lc1 = len(c1)
    lc2 = len(c2)
    if lc1 < lc2:
        return c1[:1] * 0, c1
    elif lc2 == 1:
        return c1 / c2[-1], c1[:1] * 0
    else:
        quo = np.empty(lc1 - lc2 + 1, dtype=c1.dtype)
        rem = c1
        for i in range(lc1 - lc2, - 1, -1):
            p = mul_f([0] * i + [1], c2)
            q = rem[-1] / p[-1]
            rem = rem[:-1] - q * p[:-1]
            quo[i] = q
        return quo, trimseq(rem)


def _div(x, y):
  return x / y if isinstance(x.mlir_dtype, ir.FloatType) else x.trunc_div(y)


def _div(dividend: int, divisor: int):
  if divisor == 1:
    return dividend

  return lax.div(dividend, divisor)

