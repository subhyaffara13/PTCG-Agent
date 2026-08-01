
def _restore_rng_counters(scopes, fingerprint, capture_old_counts):
  if fingerprint not in _side_effect_cache.cache:
    capture_new_counts = jax.tree.map(
        lambda s: CountsHolder.make(s.rng_counters), scopes
    )
    capture_delta_counts = jax.tree.map(
        lambda old, new: new.sub(old),
        capture_old_counts,
        capture_new_counts,
    )
    _side_effect_cache.cache[fingerprint] = capture_delta_counts
  else:
    updated_counts = jax.tree.map(
        lambda x, y: x.add(y).unflat(),
        _side_effect_cache.cache[fingerprint],
        capture_old_counts,
    )
    jax.tree.map(
        lambda s, u: set_from_dict(s.rng_counters, u),
        scopes,
        updated_counts,
    )

