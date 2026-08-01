
def _to_worker_restore_structure(tree: PyTree) -> PyTree:
  """Matches worker-side bare restore for legacy empty namedtuples."""
  # Sidecars restore with bare PyTreeRestore(), so legacy metadata restore does
  # not have the caller item needed to reconstruct zero-leaf namedtuples.
  return jax.tree.map(
      lambda x: None if _uses_legacy_empty_namedtuple_restore(x) else x,
      tree,
      is_leaf=_uses_legacy_empty_namedtuple_restore,
  )

