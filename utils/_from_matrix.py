
def _from_matrix(matrix: Array) -> Array:
  matrix_trace = matrix[0, 0] + matrix[1, 1] + matrix[2, 2]
  decision = jnp.array([matrix[0, 0], matrix[1, 1], matrix[2, 2], matrix_trace], dtype=matrix.dtype)
  choice = jnp.argmax(decision)
  i = choice
  j = (i + 1) % 3
  k = (j + 1) % 3
  quat_012 = jnp.empty(4, dtype=matrix.dtype)
  quat_012 = quat_012.at[i].set(1 - decision[3] + 2 * matrix[i, i])
  quat_012 = quat_012.at[j].set(matrix[j, i] + matrix[i, j])
  quat_012 = quat_012.at[k].set(matrix[k, i] + matrix[i, k])
  quat_012 = quat_012.at[3].set(matrix[k, j] - matrix[j, k])
  quat_3 = jnp.empty(4, dtype=matrix.dtype)
  quat_3 = quat_3.at[0].set(matrix[2, 1] - matrix[1, 2])
  quat_3 = quat_3.at[1].set(matrix[0, 2] - matrix[2, 0])
  quat_3 = quat_3.at[2].set(matrix[1, 0] - matrix[0, 1])
  quat_3 = quat_3.at[3].set(1 + decision[3])
  quat = jnp.where(choice != 3, quat_012, quat_3)
  return _normalize_quaternion(quat)

