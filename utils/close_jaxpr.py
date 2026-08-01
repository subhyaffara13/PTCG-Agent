
def close_jaxpr(jaxpr: Jaxpr) -> ClosedJaxpr:
  # The `jaxpr.replace()` is making a copy of the Jaxpr, without which
  # the cache value would have a strong reference to the same Jaxpr as
  # the key, and we would never gc the cache entry. This works because
  # Jaxpr is hashed by id, and the cache entry is dead is the key is dead.
  return ClosedJaxpr(jaxpr.replace(), ())

