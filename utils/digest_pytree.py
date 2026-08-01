
def digest_pytree(pytree: Any) -> dict[str, str]:
  """Computes a per-leaf SHA-256 digest keyed by leaf path.

  Useful for load-only benchmarks, where no in-memory reference pytree
  exists to pass to `assert_pytree_equal`: capture digests once, then check
  future loads against them with `assert_digests_match`.

  Args:
    pytree: The pytree to digest.

  Returns:
    Mapping of leaf path to the hex SHA-256 of its (dtype, shape, bytes).
  """
  leaves = jax.tree_util.tree_flatten_with_path(pytree)[0]
  digests: dict[str, str] = {}
  for keypath, leaf in leaves:
    arr = _leaf_to_numpy(leaf)
    h = hashlib.sha256()
    h.update(arr.dtype.str.encode("ascii"))
    h.update(repr(arr.shape).encode("ascii"))
    h.update(arr.tobytes())
    digests[jax.tree_util.keystr(keypath) or "<root>"] = h.hexdigest()
  return digests

