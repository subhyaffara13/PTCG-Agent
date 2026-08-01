
def hungarian_algorithm(cost_matrix):
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

  This implementation is based on that of the Scenic library (see references).

  Unlike `base_hungarian_algorithm`, this version yields a simpler Jaxpr and
  appears to be faster.

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

  References:
    Dehghani et al., `Scenic: A JAX Library for Computer Vision Research and
    Beyond <https://arxiv.org/abs/2110.11403>`_, 2022
  """

  def row_fn(state, row):

    def dfs_body_fn(state):
      u, v, used, minv, path, col = state

      # mark column as used
      used = used.at[col].set(True)
      unused_slice = ~used[1:]

      row = parent[col]

      # update minv and path to it
      cur = cost_matrix[row - 1, :] - u[row] - v[1:]
      cur = jnp.where(unused_slice, cur, jnp.inf)
      path = jnp.where(cur < minv, col, path)
      minv = jnp.where(cur < minv, cur, minv)  # type: ignore

      # mask out the visited rows
      col = _masked_argmin(minv, unused_slice) + 1
      delta = minv.min(where=unused_slice, initial=jnp.inf)

      # update potentials
      indices = jnp.where(used, parent, rows + 1)  # out-of-bounds
      u = u.at[indices].add(delta)
      v = jnp.where(used, v - delta, v)
      minv = jnp.where(unused_slice, minv - delta, minv)

      return u, v, used, minv, path, col

    def dfs_cond_fn(state):
      _, _, _, _, _, col = state
      return parent[col] != 0

    def back_body_fn(state):
      parent, old_col = state
      new_col = path[old_col - 1]
      parent = parent.at[old_col].set(parent[new_col])
      return parent, new_col

    def back_cond_fn(state):
      _, col = state
      return col != 0

    u, v, parent = state
    parent = parent.at[0].set(row + 1)

    # run the inner while loop (i.e. DFS)
    path = jnp.zeros(cols, int)
    used = jnp.zeros(cols + 1, bool)
    minv = jnp.full(cols, jnp.inf)  # support array
    col = 0

    # update parents based on the DFS path
    state = u, v, used, minv, path, col
    state = lax.while_loop(dfs_cond_fn, dfs_body_fn, state)
    u, v, _, _, path, col = state

    # backtrack the DFS path
    parent, _ = lax.while_loop(back_cond_fn, back_body_fn, (parent, col))

    return (u, v, parent), None

  if cost_matrix.shape[0] == 0 or cost_matrix.shape[1] == 0:
    return jnp.zeros(0, int), jnp.zeros(0, int)

  transpose = cost_matrix.shape[0] > cost_matrix.shape[1]

  if transpose:
    cost_matrix = cost_matrix.T

  rows, cols = cost_matrix.shape

  u = jnp.zeros(rows + 2)  # row potential
  v = jnp.zeros(cols + 1)  # column potential
  parent = jnp.zeros(cols + 1, int)  # maps columns to rows

  # loop over the rows of the cost matrix
  (u, v, parent), _ = lax.scan(row_fn, (u, v, parent), jnp.arange(rows))
  # -v[0] is the matching cost

  # top_k is costly, so skip it when possible (i.e. for square matrices)
  if rows == cols:
    parent, indices = parent[1:], jnp.arange(rows)
  else:
    parent, indices = lax.top_k(parent[1:], rows)

  parent -= 1  # switch back to 0-based indexing

  if transpose:
    return indices, parent

  return parent, indices

