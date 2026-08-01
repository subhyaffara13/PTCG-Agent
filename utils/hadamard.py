
def hadamard(n, dtype=int):
    """
    Construct a Hadamard matrix.

    Constructs an n-by-n Hadamard matrix, using Sylvester's
    construction. `n` must be a power of 2.

    Parameters
    ----------
    n : int
        The order of the matrix. `n` must be a power of 2.
    dtype : dtype, optional
        The data type of the array to be constructed.

    Returns
    -------
    H : (n, n) ndarray
        The Hadamard matrix.

    Notes
    -----
    .. versionadded:: 0.8.0

    Examples
    --------
    >>> from scipy.linalg import hadamard
    >>> hadamard(2, dtype=complex)
    array([[ 1.+0.j,  1.+0.j],
           [ 1.+0.j, -1.-0.j]])
    >>> hadamard(4)
    array([[ 1,  1,  1,  1],
           [ 1, -1,  1, -1],
           [ 1,  1, -1, -1],
           [ 1, -1, -1,  1]])

    """

    # This function is a slightly modified version of the
    # function contributed by Ivo in ticket #675.

    if n < 1:
        lg2 = 0
    else:
        lg2 = int(math.log(n, 2))
    if 2 ** lg2 != n:
        raise ValueError("n must be a positive integer, and n must be "
                         "a power of 2")

    H = np.array([[1]], dtype=dtype)

    # Sylvester's construction
    for i in range(0, lg2):
        H = np.vstack((np.hstack((H, H)), np.hstack((H, -H))))

    return H


def hadamard(n: int, dtype: DTypeLike = int) -> Array:
  r"""Construct an n-by-n Hadamard matrix.

  JAX implementation of :func:`scipy.linalg.hadamard`.

  For ``n`` a positive power of 2, the Hadamard matrix :math:`H_n` satisfies
  :math:`H_n H_n^T = n I`. It is defined recursively by the Sylvester
  construction: :math:`H_1 = [[1]]`, and
  :math:`H_{2m} = \begin{bmatrix} H_m & H_m \\ H_m & -H_m \end{bmatrix}`.

  Args:
    n: size of the matrix. Must be a positive power of 2.
    dtype: output dtype. Defaults to ``int``.

  Returns:
    A Hadamard matrix of shape ``(n, n)``.

  Examples:
    >>> jax.scipy.linalg.hadamard(4)
    Array([[ 1,  1,  1,  1],
           [ 1, -1,  1, -1],
           [ 1,  1, -1, -1],
           [ 1, -1, -1,  1]], dtype=int32)
  """
  if n < 1 or not math.log2(n).is_integer():
    raise ValueError(
        f"n must be a positive power of 2; got {n}.")
  lg2 = int(math.log2(n))
  H = jnp.ones((1, 1), dtype=dtype)
  for _ in range(lg2):
    H = jnp.block([[H, H], [H, -H]])
  return H

