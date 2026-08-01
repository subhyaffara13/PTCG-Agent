
def _handle_scalar_broadcasting(nd, x, d):
  # Callers of this utility, via broadcast_batcher() or defbroadcasting(),
  # must be in a context where lax is importable.
  from jax import lax  # pyrefly: ignore[missing-module-attribute]
  return (x if d is None or nd == np.ndim(x) else
          lax.expand_dims(x, tuple(range(np.ndim(x), nd))))

