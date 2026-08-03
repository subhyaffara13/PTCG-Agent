import math


def rand_indices_unique_along_axis(rng):
  """Sample an array of given shape containing indices up to dim (exclusive),
  such that the indices are unique along the given axis.
  Optionally, convert some of the resulting indices to negative indices."""
  def fn(dim, shape, axis, allow_negative=True):
    batch_size = math.prod(shape[:axis] + shape[axis:][1:])
    idx = [
      rng.choice(dim, size=shape[axis], replace=False)
      for _ in range(batch_size)
    ]
    idx = np.array(idx).reshape(batch_size, shape[axis])
    idx = idx.reshape(shape[:axis] + shape[axis:][1:] + (shape[axis],))
    idx = np.moveaxis(idx, -1, axis)

    # assert that indices are unique along the given axis
    count = partial(np.bincount, minlength=dim)
    assert (np.apply_along_axis(count, axis, idx) <= 1).all()

    if allow_negative:
      mask = rng.choice([False, True], idx.shape)
      idx[mask] -= dim
    return idx

  return fn

