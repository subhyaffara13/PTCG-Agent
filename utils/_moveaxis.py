
def _moveaxis(src, dst, x):
  perm = [i for i in range(x.ndim) if i != src]
  perm.insert(dst, src)
  return lax.transpose(x, perm)


def _moveaxis(a: Array, source: tuple[int, ...], destination: tuple[int, ...]) -> Array:
  source = tuple(_canonicalize_axis(i, np.ndim(a)) for i in source)
  destination = tuple(_canonicalize_axis(i, np.ndim(a)) for i in destination)
  if len(source) != len(destination):
    raise ValueError("Inconsistent number of elements: {} vs {}"
                     .format(len(source), len(destination)))
  perm = [i for i in range(np.ndim(a)) if i not in source]
  for dest, src in sorted(zip(destination, source)):
    perm.insert(dest, src)
  return lax.transpose(a, perm)


def _moveaxis(a: ArrayLike, source: int, destination: int) -> Array:
  # simplified version of jnp.moveaxis() for local use.
  a = ensure_arraylike("moveaxis", a)
  source = canonicalize_axis(source, np.ndim(a))
  destination = canonicalize_axis(destination, np.ndim(a))
  perm = [i for i in range(np.ndim(a)) if i != source]
  perm.insert(destination, source)
  return lax.transpose(a, perm)

