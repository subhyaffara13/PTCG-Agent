
def is_range_out_of_bounds_for_shape(
    rnge: tuple[slice | int, ...], shape: tuple[int, ...]
) -> bool:
  """Returns whether `rnge` is at least partially out of bounds for `shape`."""
  for d, r in zip(shape, rnge, strict=True):
    if isinstance(r, int):
      assert 0 <= r
      if r >= d:
        return True
    elif isinstance(r, slice):
      assert r.start is not None and 0 <= r.start
      assert r.stop is not None and 0 <= r.stop

      if r.step is None:
        if r.stop > d:
          return True
      else:
        assert 0 <= r.step
        num_elements_in_slice = (r.stop - r.start + r.step - 1) // r.step
        if num_elements_in_slice > 0:
          last_index = r.start + (num_elements_in_slice - 1) * r.step
          if last_index >= d:
            return True
    else:
      raise ValueError(f"Unsupported range type: {type(r)}.")
  return False

