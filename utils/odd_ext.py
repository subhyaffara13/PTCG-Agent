
def odd_ext(x, n, axis=-1):
    """
    Odd extension at the boundaries of an array

    Generate a new ndarray by making an odd extension of `x` along an axis.

    Parameters
    ----------
    x : ndarray
        The array to be extended.
    n : int
        The number of elements by which to extend `x` at each end of the axis.
    axis : int, optional
        The axis along which to extend `x`. Default is -1.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.signal._arraytools import odd_ext
    >>> a = np.array([[1, 2, 3, 4, 5], [0, 1, 4, 9, 16]])
    >>> odd_ext(a, 2)
    array([[-1,  0,  1,  2,  3,  4,  5,  6,  7],
           [-4, -1,  0,  1,  4,  9, 16, 23, 28]])

    Odd extension is a "180 degree rotation" at the endpoints of the original
    array:

    >>> t = np.linspace(0, 1.5, 100)
    >>> a = 0.9 * np.sin(2 * np.pi * t**2)
    >>> b = odd_ext(a, 40)
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(np.arange(-40, 140), b, 'b', lw=1, label='odd extension')
    >>> plt.plot(np.arange(100), a, 'r', lw=2, label='original')
    >>> plt.legend(loc='best')
    >>> plt.show()
    """
    if n < 1:
        return x
    if n > x.shape[axis] - 1:
        raise ValueError(("The extension length n (%d) is too big. " +
                         "It must not exceed x.shape[axis]-1, which is %d.")
                         % (n, x.shape[axis] - 1))
    left_end = axis_slice(x, start=0, stop=1, axis=axis)
    left_ext = axis_slice(x, start=n, stop=0, step=-1, axis=axis)
    right_end = axis_slice(x, start=-1, axis=axis)
    right_ext = axis_slice(x, start=-2, stop=-(n + 2), step=-1, axis=axis)
    ext = np.concatenate((2 * left_end - left_ext,
                          x,
                          2 * right_end - right_ext),
                         axis=axis)
    return ext


def odd_ext(x: Array, n: int, axis: int = -1) -> Array:
  """Extends `x` along with `axis` by odd-extension.

  This function was previously a part of "scipy.signal.signaltools" but is no
  longer exposed.

  Args:
    x : input array
    n : the number of points to be added to the both end
    axis: the axis to be extended
  """
  if n < 1:
    return x
  if n > x.shape[axis] - 1:
    raise ValueError(
        f"The extension length n ({n}) is too big. "
        f"It must not exceed x.shape[axis]-1, which is {x.shape[axis] - 1}.")
  left_end = lax.slice_in_dim(x, 0, 1, axis=axis)
  left_ext = jnp.flip(lax.slice_in_dim(x, 1, n + 1, axis=axis), axis=axis)
  right_end = lax.slice_in_dim(x, -1, None, axis=axis)
  right_ext = jnp.flip(lax.slice_in_dim(x, -(n + 1), -1, axis=axis), axis=axis)
  ext = jnp.concatenate((2 * left_end - left_ext,
                         x,
                         2 * right_end - right_ext),
                         axis=axis)
  return ext

