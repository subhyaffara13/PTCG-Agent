
def _einshape(
    equation: str,
    value: jax_typing.Array,
    **sizes: int,
) -> jax_typing.Array:
  """Reshapes and transposes an array according to an einshape equation.

  Args:
    equation: String of the form "ab(cd)->cabd". Parentheses indicate grouping
      of dimensions. On the LHS, grouped dimensions are split. On the RHS,
      dimensions are merged.
    value: The array to reshape.
    **sizes: Integer sizes for dimensions that are split and cannot be inferred.

  Returns:
    The reshaped and transposed array.
  """
  transforms = get_einshape_transforms(equation, value.shape, **sizes)
  for transform in transforms:
    match transform:
      case SplitDims(_, _):
        new_shape = transform.transform_shape(value.shape)
        value = value.reshape(new_shape)
      case MergeDims(_, _):
        new_shape = transform.transform_shape(value.shape)
        value = value.reshape(new_shape)
      case Transpose(permutation):
        value = lax.transpose(value, permutation)
  return value

