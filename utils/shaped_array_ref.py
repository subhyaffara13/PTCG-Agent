
def shaped_array_ref(
    shape: tuple[int, ...], dtype, weak_type: bool = False) -> AbstractRef:
  return AbstractRef(core.ShapedArray(shape, dtype, weak_type=weak_type))

