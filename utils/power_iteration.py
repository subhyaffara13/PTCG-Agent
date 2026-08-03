import functools
from typing import Callable, Optional, Union

def power_iteration(
    matrix: Union[
        jax.typing.ArrayLike, Callable[[base.ArrayTree], base.ArrayTree]],
    *,
    v0: Optional[base.ArrayTree] = None,
    num_iters: jax.typing.ArrayLike = 100,
    error_tolerance: jax.typing.ArrayLike = 1e-6,
    precision: lax.Precision = lax.Precision.HIGHEST,
    key: Optional[base.PRNGKey] = None,
) -> tuple[jax.typing.ArrayLike, base.ArrayTree]:
  r"""Power iteration algorithm.

  This algorithm computes the dominant eigenvalue (i.e. the spectral radius) and
  its associated eigenvector of a diagonalizable matrix. This matrix can be
  given as an array or as a callable implementing a matrix-vector product.

  Args:
    matrix: a square matrix, either as an array or a callable implementing a
      matrix-vector product.
    v0: initial vector approximating the dominiant eigenvector. If ``matrix`` is
      an array of size (n, n), v0 must be a vector of size (n,). If instead
      ``matrix`` is a callable, then v0 must be a tree with the same structure
      as the input of this callable. If this argument is None and ``matrix`` is
      an array, then a random vector sampled from a uniform distribution in [-1,
      1] is used as initial vector.
    num_iters: Number of power iterations.
    error_tolerance: Iterative exit condition. The procedure stops when the
      relative error of the estimate of the dominant eigenvalue is below this
      threshold.
    precision: precision XLA related flag, the available options are: a)
      lax.Precision.DEFAULT (better step time, but not precise); b)
      lax.Precision.HIGH (increased precision, slower); c) lax.Precision.HIGHEST
      (best possible precision, slowest).
    key: random key for the initialization of ``v0`` when not given explicitly.
      When this argument is None, `jax.random.PRNGKey(0)` is used.

  Returns:
    A pair (eigenvalue, eigenvector), where eigenvalue is the dominant
    eigenvalue of ``matrix`` and eigenvector is its associated eigenvector.

  References:
    Wikipedia contributors. `Power iteration
    <https://en.wikipedia.org/w/index.php?tit0le=Power_iteration>`_.

  .. note::
    If the matrix is not diagonalizable or the dominant eigenvalue is not
    unique, the algorithm may not converge.

  .. versionchanged:: 0.2.2
    ``matrix`` can be a callable. Reversed the order of the return parameters,
    from (eigenvector, eigenvalue) to (eigenvalue, eigenvector).
  """
  if callable(matrix):
    mvp = matrix
    if v0 is None:
      # v0 must be given as we don't know the underlying pytree structure.
      raise ValueError('v0 must be provided when `matrix` is a callable.')
  else:
    mvp = lambda v: jnp.matmul(matrix, v, precision=precision)
    if v0 is None:
      if key is None:
        key = jax.random.PRNGKey(0)
      # v0 is uniformly distributed in [-1, 1]
      v0 = jax.random.uniform(
          key,
          shape=matrix.shape[-1:],
          dtype=matrix.dtype,
          minval=-1.0,
          maxval=1.0,
      )

  v0 = _normalize_tree(v0)

  cond_fun = functools.partial(
      _power_iteration_cond_fun,
      error_tolerance,
      num_iters,
  )

  def _body_fun(loop_vars):
    _, z, _, iter_num = loop_vars
    eigvec = _normalize_tree(z)
    z = mvp(eigvec)
    eig = optax.tree.vdot(eigvec, z)
    return eigvec, z, eig, iter_num + 1

  init_vars = (v0, mvp(v0), jnp.asarray(0.0), jnp.asarray(0))
  _, unormalized_eigenvector, dominant_eigenvalue, _ = jax.lax.while_loop(
      cond_fun, _body_fun, init_vars
  )
  normalized_eigenvector = _normalize_tree(unormalized_eigenvector)
  return dominant_eigenvalue, normalized_eigenvector

