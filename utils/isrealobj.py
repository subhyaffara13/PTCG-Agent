from typing import Any

def isrealobj(x: ArrayLike):
    return not torch.is_complex(x)


def isrealobj(x):
    """
    Return True if x is a not complex type or an array of complex numbers.

    The type of the input is checked, not the value. So even if the input
    has an imaginary part equal to zero, `isrealobj` evaluates to False
    if the data type is complex.

    Parameters
    ----------
    x : any
        The input can be of any type and shape.

    Returns
    -------
    y : bool
        The return value, False if `x` is of a complex type.

    See Also
    --------
    iscomplexobj, isreal

    Notes
    -----
    The function is only meant for arrays with numerical values but it
    accepts all other objects. Since it assumes array input, the return
    value of other objects may be True.

    >>> np.isrealobj('A string')
    True
    >>> np.isrealobj(False)
    True
    >>> np.isrealobj(None)
    True

    Examples
    --------
    >>> import numpy as np
    >>> np.isrealobj(1)
    True
    >>> np.isrealobj(1+0j)
    False
    >>> np.isrealobj([3, 1+0j, True])
    False

    """
    return not iscomplexobj(x)


def isrealobj(x: Any) -> bool:
  """Check if the input is not a complex number or an array containing complex elements.

  JAX implementation of :func:`numpy.isrealobj`.

  The function evaluates based on input type rather than value.
  Inputs with zero imaginary parts are still considered complex.

  Args:
    x: input object to check.

  Returns:
    False if ``x`` is a complex number or an array containing at least one complex element,
    True otherwise.

  See Also:
    - :func:`jax.numpy.iscomplexobj`
    - :func:`jax.numpy.isreal`

  Examples:
    >>> jnp.isrealobj(0)
    True
    >>> jnp.isrealobj(1.2)
    True
    >>> jnp.isrealobj(jnp.array([1, 2]))
    True
    >>> jnp.isrealobj(1+2j)
    False
    >>> jnp.isrealobj(jnp.array([0, 1+2j]))
    False
  """
  return not iscomplexobj(x)

