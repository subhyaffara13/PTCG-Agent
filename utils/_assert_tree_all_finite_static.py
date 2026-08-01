
def _assert_tree_all_finite_static(tree_like: ArrayTree) -> None:
  """Checks that all leaves in a tree are finite.

  Args:
    tree_like: A pytree with array leaves.

  Raises:
    AssertionError: If any leaf in ``tree_like`` is non-finite.
  """
  all_finite = jax.tree_util.tree_all(
      jax.tree_util.tree_map(lambda x: np.all(np.isfinite(x)), tree_like))
  if not all_finite:
    is_finite = lambda x: "Finite" if np.all(np.isfinite(x)) else "Nonfinite"
    error_msg = jax.tree.map(is_finite, tree_like)
    raise AssertionError(f"Tree contains non-finite value: {error_msg}.")

