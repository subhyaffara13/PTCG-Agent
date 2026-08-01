
def diff_tracing_cache_keys(new_key, old_key) -> tuple[int, int, str]:
  """Explain the diff between two tracing cache keys.
  Returns:
    A tuple of (severity, num_diffs, explanation) for the diff between the two
    keys. Severity is an int, where lower is better.
  """
  new_ctx, (new_tree, new_dbg, *_), () = new_key
  old_ctx, (old_tree, old_dbg, *_), () = old_key
  return (diff_tracing_ctx(new_ctx, old_ctx) or
          diff_trees(new_tree.tree, old_tree.tree) or
          diff_debug(new_dbg, old_dbg) or
          diff_types(new_dbg, new_tree.vals, old_tree.vals) or
          (4, 0, 'cache miss explanation unavailable'))

