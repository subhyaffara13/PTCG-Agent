
def _broadcast_to(array, shape, subok, readonly):
    shape = tuple(shape) if np.iterable(shape) else (shape,)
    array = np.array(array, copy=None, subok=subok)
    if not shape and array.shape:
        raise ValueError('cannot broadcast a non-scalar to a scalar array')
    if any(size < 0 for size in shape):
        raise ValueError('all elements of broadcast shape must be non-'
                         'negative')
    extras = []
    it = np.nditer(
        (array,), flags=['multi_index', 'refs_ok', 'zerosize_ok'] + extras,
        op_flags=['readonly'], itershape=shape, order='C')
    with it:
        # never really has writebackifcopy semantics
        broadcast = it.itviews[0]
    result = _maybe_view_as_subclass(array, broadcast)
    # In a future version this will go away
    if not readonly and array.flags._writeable_no_warn:
        result.flags.writeable = True
        result.flags._warn_on_write = True
    return result


def _broadcast_to(x: Array, shape: tuple[int, ...]) -> Array:
  assert x.ndim <= len(shape)
  return lax.broadcast_in_dim(x, shape, range(len(shape) - x.ndim, len(shape)))


def _broadcast_to(arr: ArrayLike, shape: DimSize | Shape, sharding=None
                  ) -> Array:
  arr = ensure_arraylike("broadcast_to", arr)
  if not isinstance(shape, tuple) and np.ndim(shape) == 0:
    shape = (shape,)
  # check that shape is concrete
  shape = core.canonicalize_shape(shape)  # pyrefly: ignore[bad-argument-type]
  sharding = canonicalize_sharding(sharding, 'jnp.broadcast_to')
  return lax.broadcast_to(arr, shape, sharding)

