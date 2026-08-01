
def set_diags(a: jax.Array, new_diags: jax.typing.ArrayLike) -> jax.Array:
  """Set the diagonals of every DxD matrix in an input of shape NxDxD.

  Args:
    a: rank 3, tensor NxDxD.
    new_diags: NxD matrix, the new diagonals of each DxD matrix.

  Returns:
    NxDxD tensor, with the same contents as `a` but with the diagonal
      changed to `new_diags`.
  """
  a_dim, new_diags_dim = len(a.shape), len(new_diags.shape)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  if a_dim != 3:
    raise ValueError(f'Expected `a` to be a 3D tensor, got {a_dim}D instead')
  if new_diags_dim != 2:
    raise ValueError(
        f'Expected `new_diags` to be a 2D array, got {new_diags_dim}D instead'
    )
  n, d, d1 = a.shape
  n_diags, d_diags = new_diags.shape  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  if d != d1:
    raise ValueError(
        f'Shape mismatch: expected `a.shape` to be {(n, d, d)}, '
        f'got {(n, d, d1)} instead'
    )
  if d_diags != d or n_diags != n:
    raise ValueError(
        f'Shape mismatch: expected `new_diags.shape` to be {(n, d)}, '
        f'got {(n_diags, d_diags)} instead'
    )

  indices1 = jnp.repeat(jnp.arange(n), d)
  indices2 = jnp.tile(jnp.arange(d), n)
  indices3 = indices2

  # Use numpy array setting
  a = a.at[indices1, indices2, indices3].set(new_diags.flatten())  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  return a

