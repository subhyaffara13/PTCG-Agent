
def base_hungarian_algorithm(cost_matrix):
  r"""The Hungarian algorithm for the linear assignment problem.

  In `this problem <https://en.wikipedia.org/wiki/Linear_assignment_problem>`_,
  we are given an :math:`n \times m` cost matrix. The goal is to compute an
  assignment, i.e. a set of pairs of rows and columns, in such a way that:

  - At most one column is assigned to each row.
  - At most one row is assigned to each column.
  - The total number of assignments is :math:`\min(n, m)`.
  - The assignment minimizes the sum of costs.

  Equivalently, given a weighted complete bipartite graph, the problem is to
  find a maximum-cardinality matching that minimizes the sum of the weights of
  the edges included in the matching.

  Formally, the problem is as follows. Given :math:`C \in \mathbb{R}^{n \times m
  }`, solve the following `integer linear program <https://en.wikipedia.org/wiki
  /Integer_linear_program>`_:

  .. math::

    \begin{align*}
        \text{minimize} \quad & \sum_{i \in [n]} \sum_{j \in [m]} C_{ij} X_{ij}
        \\ \text{subject to} \quad
        & X_{ij} \in \{0, 1\} & \forall i \in [n], j \in [m] \\
        & \sum_{i \in [n]} X_{ij} \leq 1 & \forall j \in [m] \\
        & \sum_{j \in [m]} X_{ij} \leq 1 & \forall i \in [n] \\
        & \sum_{i \in [n]} \sum_{j \in [m]} X_{ij} = \min(n, m)
    \end{align*}

  The `Hungarian algorithm <https://en.wikipedia.org/wiki/Hungarian_algorithm>`_
  is a cubic-time algorithm that solves this problem.

  This implementation of the Hungarian algorithm is based on the pseudocode
  presented in pages 1685-1686 of the IEEE paper cited below.

  Args:
    cost_matrix: A matrix of costs.

  Returns:
    A pair ``(i, j)`` where ``i`` is an array of row indices and ``j`` is an
    array of column indices.
    The cost of the assignment is ``cost_matrix[i, j].sum()``.

  Examples:
    >>> import optax
    >>> from jax import numpy as jnp
    >>> cost = jnp.array(
    ...  [
    ...    [8, 4, 7],
    ...    [5, 2, 3],
    ...    [9, 6, 7],
    ...    [9, 4, 8],
    ...  ])
    >>> i, j = optax.assignment.hungarian_algorithm(cost)
    >>> print("cost:", cost[i, j].sum())
    cost: 15
    >>> print("i:", i)
    i: [0 1 3]
    >>> print("j:", j)
    j: [0 2 1]
    >>> cost = jnp.array(
    ...  [
    ...    [90, 80, 75, 70],
    ...    [35, 85, 55, 65],
    ...    [125, 95, 90, 95],
    ...    [45, 110, 95, 115],
    ...    [50, 100, 90, 100],
    ...  ])
    >>> i, j = optax.assignment.hungarian_algorithm(cost)
    >>> print("cost:", cost[i, j].sum())
    cost: 265
    >>> print("i:", i)
    i: [0 1 2 3]
    >>> print("j:", j)
    j: [3 2 1 0]

  References:
    David F. Crouse, `On implementing 2D rectangular assignment algorithms
    <https://ieeexplore.ieee.org/document/7738348>`_, 2016
  """

  if cost_matrix.shape[0] == 0 or cost_matrix.shape[1] == 0:
    return jnp.zeros(0, int), jnp.zeros(0, int)

  transpose = cost_matrix.shape[1] < cost_matrix.shape[0]

  if transpose:
    cost_matrix = cost_matrix.T

  cost_matrix = cost_matrix.astype(float)
  u = jnp.zeros(cost_matrix.shape[0], cost_matrix.dtype)
  v = jnp.zeros(cost_matrix.shape[1], cost_matrix.dtype)

  path = jnp.full(cost_matrix.shape[1], -1)
  col4row = jnp.full(cost_matrix.shape[0], -1)
  row4col = jnp.full(cost_matrix.shape[1], -1)

  init = cost_matrix, u, v, path, row4col, col4row
  cost_matrix, _, _, _, _, col4row = jax.lax.fori_loop(
      0, cost_matrix.shape[0], _lsa_body, init
  )

  if transpose:
    i = col4row.argsort()
    return col4row[i], i
  else:
    return jnp.arange(cost_matrix.shape[0]), col4row

