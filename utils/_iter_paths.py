
def _iter_paths(tree: PyTreeDef, specs: Specs, fails: list[T | NoFail]
                ) -> list[tuple[tuple[KeyPath, P], tuple[KeyPath, T]]]:
  failures = tree_unflatten(tree, fails)
  failures_aug = generate_key_paths(failures)
  specs_ = tree_unflatten(tree_structure(specs), map(Tup, generate_key_paths(specs)))
  specs_aug = broadcast_prefix(specs_, failures, is_leaf=lambda x: x is None)
  return [(s, (fail_key, fail_data)) for s, (fail_key, fail_data)
          in zip(specs_aug, failures_aug)
          if s is not None and fail_data is not no_fail]

