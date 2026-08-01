
def repeat_by_pattern(
    *,
    pattern: str,
    dimension: int,
    repeat_count: int,
) -> Transformation:
  r"""Repeats parameters by finding keys that match a regex pattern.

  Example:
      pattern = r"^(.*)\\.weight$"
      dimension = 1
      repeat_count = 2

        Transforms:
          "model.layers.0.weight": [[1, 2], [3, 4]]
        Into:
          "model.layers.0.weight": [[1, 1, 2, 2], [3, 3, 4, 4]]

  Args:
      pattern: Regex to filter keys that will be repeated.
      dimension: The axis/dimension to repeat along.
      repeat_count: Number of times to repeat elements.

  Returns:
      A Transformation function.
  """
  compiled_pattern = re.compile(pattern)

  def transform(
      *params: types.PyTreeOf[jax.Array],
  ) -> types.PyTreeOf[jax.Array]:
    if len(params) > 1:
      raise ValueError(
          "Can only repeat parameters in a single parameter structure."
      )
    params = params[0]
    result = dict(params)
    del params

    for key in result:
      if compiled_pattern.match(key):
        result[key] = _repeat_val(result[key], dimension, repeat_count)

    return result

  return transform

