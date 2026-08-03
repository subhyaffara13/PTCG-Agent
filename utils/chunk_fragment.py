import itertools

def chunk_fragment(fragment: F, target_shape: Shape) -> list[F]:
  """Chunks the given fragment into the given target shape.

  Args:
    fragment: The fragment to chunk. Fragment's shape must be divisible by the
      target shape. If the fragment is concrete (has a value), the operation is
      zero copy and the returned fragments will have the same underlying buffer.
    target_shape: The shape to chunk the fragment into.

  Returns:
    A list of fragments that cover the entire original fragment, each of
    target_shape shape.

    The order of the returned fragments is deterministic: the index of the
    innermost axis changes fastest. For example: a fragment with index
    [0:4:2, 0:2:1] and target_shape [2, 1] will be split into fragments
    with indices ordered as follows:
      [[0:2:1, 0:1:1], [0:2:1, 1:2:1], [2:4:1, 0:1:1], [2:4:1, 1:2:1]]

  Raises:
    ValueError: If the fragment's shape is not divisible by the target shape.
  """
  fragment_t = type(fragment)

  if fragment.shape == target_shape:
    return [fragment]

  if len(target_shape) != len(fragment.shape):
    raise ValueError(
        f'target_shape={target_shape} must have the same length as'
        f' fragment.shape={fragment.shape}'
    )
  if not validate_divisible_shapes(fragment.shape, target_shape):
    raise ValueError(
        f'fragment.shape={fragment.shape} is not divisible by'
        f' target_shape={target_shape}'
    )

  start_indices_per_dim = (
      range(start, stop, new_dim)
      for start, stop, new_dim in zip(
          fragment.start, fragment.stop, target_shape, strict=True
      )
  )
  start_indices = itertools.product(*start_indices_per_dim)
  new_fragments = []
  for start_index in start_indices:
    new_index = tuple(
        slice(start_index[i], start_index[i] + target_shape[i], 1)
        for i in range(len(target_shape))
    )
    if fragment.value is None:
      value = None
    else:
      value_index = (
          fragments_lib.AbstractFragment(index=new_index)
          .offset_by(-fragment.start)
          .index
      )
      value = fragment.value[value_index]
    new_fragments.append(fragment_t(index=new_index, value=value))
  return new_fragments

