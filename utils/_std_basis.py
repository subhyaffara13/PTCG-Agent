
def _std_basis(pytree):
  import jax.numpy as jnp  # pyrefly: ignore[missing-import]
  leaves, _ = tree_flatten(pytree)
  ndim = sum(map(np.size, leaves))
  dtype = dtypes.result_type(*leaves)
  flat_basis = jnp.eye(ndim, dtype=dtype)
  axis = 1
  arr_s = [None] * flat_basis.ndim
  specs = tree_map(lambda l: P(arr_s[:axis], *core.typeof(l).sharding.spec,
                               arr_s[axis+1:]), pytree)
  out_pytree = _unravel_array_into_pytree(pytree, axis, None, flat_basis, specs)
  out_pytree = tree_map(_insert_pvary, out_pytree, pytree)
  return out_pytree

