
def dissolve_slice(
    xs: NdSlice,
    shape: Shape,
    preserve_rank: bool = True,
) -> NdSlice:
  """Turns an N-dimensional slice into an equivalent one with `None`s in it.

  Invariant: `a[dissolve_slice(xs, a.shape)] == a[xs]`.

  This is the inverse of `resolve_slice()`.

  Args:
    xs: The slice to simplify.
    shape: The shape against which to simplify.
    preserve_rank: If false, remove any redundant `slice(None)` elements from
      the tail of the result.

  Returns:
    An N-dimensional slice that, when applied to an array of shape `shape`,
    has the same effect as `xs`, but that has `None` wherever possible in its
    constituent slices.
  """
  ys = tuple(
      slice(x.start or None,
            x.stop if x.stop != dim else None,
            x.step if x.step != 1 else None) for x, dim in zip(xs, shape))
  if not preserve_rank:
    while ys and ys[-1] == slice(None):
      ys = ys[:-1]
  return ys if ys else Ellipsis

