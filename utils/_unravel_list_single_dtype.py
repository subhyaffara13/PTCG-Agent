
def _unravel_list_single_dtype(sizes: Sizes, shapes: Shapes, arr: Array) -> list[Array]:
  chunks = lax.split(arr, sizes)
  return [chunk.reshape(shape) for chunk, shape in zip(chunks, shapes)]

