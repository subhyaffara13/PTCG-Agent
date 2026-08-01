
def _canonicalize_reshape(
    input_shape: tuple[int, ...], shape: tuple[int, ...]
) -> tuple[int, ...]:
  num_negative_ones = sum(s == -1 for s in shape)
  if num_negative_ones == 0:
    if np.prod(shape) != np.prod(input_shape):
      raise ValueError(
          f"cannot reshape shape {input_shape} into shape {shape}"
      )
    return shape
  num_elements = math.prod(input_shape)
  defined_dims = [d for d in shape if d != -1]
  if len(defined_dims) != len(shape) - 1:
    raise ValueError(f"At most one dimension can be -1, but got {shape}")
  if num_elements % math.prod(defined_dims):
    raise ValueError(
        f"Specified dims {shape} do not evenly divide the size of the "
        f"ref ({num_elements})."
    )
  remaining_dim = num_elements // math.prod(defined_dims)
  return tuple(d if d != -1 else remaining_dim for d in shape)

