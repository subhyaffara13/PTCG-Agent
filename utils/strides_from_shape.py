
def strides_from_shape(shape: tuple[int, ...]) -> tuple[int, ...]:
  size = np.prod(shape)
  strides = []
  for s in shape:
    size = size // s
    strides.append(int(size))
  return tuple(strides)

