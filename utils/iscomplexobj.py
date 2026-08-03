from typing import Any

def iscomplexobj(x: ArrayLike):
    return torch.is_complex(x)


def iscomplexobj(x):
    """
    Check for a complex type or an array of complex numbers.

    The type of the input is checked, not the value. Even if the input
    has an imaginary part equal to zero, `iscomplexobj` evaluates to True.

    Parameters
    ----------
    x : any
        The input can be of any type and shape.

    Returns
    -------
    iscomplexobj : bool
        The return value, True if `x` is of a complex type or has at least
        one complex element.

    See Also
    --------
    isrealobj, iscomplex

    Examples
    --------
    >>> import numpy as np
    >>> np.iscomplexobj(1)
    False
    >>> np.iscomplexobj(1+0j)
    True
    >>> np.iscomplexobj([3, 1+0j, True])
    True

    """
    try:
        dtype = x.dtype
        type_ = dtype.type
    except AttributeError:
        type_ = asarray(x).dtype.type
    return issubclass(type_, _nx.complexfloating)


def iscomplexobj(x: Any) -> bool:
  """Check if the input is a complex number or an array containing complex elements.

  JAX implementation of :func:`numpy.iscomplexobj`.

  The function evaluates based on input type rather than value.
  Inputs with zero imaginary parts are still considered complex.

  Args:
    x: input object to check.

  Returns:
    True if ``x`` is a complex number or an array containing at least one complex element,
    False otherwise.

  See Also:
    - :func:`jax.numpy.isrealobj`
    - :func:`jax.numpy.iscomplex`

  Examples:
    >>> jnp.iscomplexobj(True)
    False
    >>> jnp.iscomplexobj(0)
    False
    >>> jnp.iscomplexobj(jnp.array([1, 2]))
    False
    >>> jnp.iscomplexobj(1+2j)
    True
    >>> jnp.iscomplexobj(jnp.array([0, 1+2j]))
    True
  """
  # Fast path for common types.
  if isinstance(x, (complex, np.complexfloating)):
    return True
  if x is None or isinstance(x, (bool, int, float, str, np.generic)):
    return False
  # Fall back to dtype attribute lookup.
  try:
    typ = x.dtype.type
  except AttributeError:
    typ = asarray(x).dtype.type
  return issubdtype(typ, np.complexfloating)

