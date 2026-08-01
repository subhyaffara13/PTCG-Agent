
def resolve_slice(xs: NdSlice, shape: Shape) -> NdSlice:
  """Turns an N-dimensional slice into an equivalent one with no `None` in it.

  Invariant: `a[dissolve_slice(xs, a.shape)] == a[xs]`.

  Args:
    xs: The slice to make explicit.
    shape: The shape against which to evaluate the slice's effect.

  Returns:
    An N-dimensional slice that, when applied to an array of shape `shape`,
    has the same effect as `xs`, but that has no `None` in any of its
    constituent slices.
  """
  return tuple(
      slice(*x.indices(n))
      if isinstance(x, slice) else slice(x, x+1, 1)
      for x, n in zip(() if xs is Ellipsis else xs, shape))

