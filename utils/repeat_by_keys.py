import logging

def repeat_by_keys(
    *,
    target_keys: Sequence[str],
    dimension: int,
    repeat_count: int,
) -> Transformation:
  """Repeats specific target keys.

  Example::
      target_keys = ["layer0.weight"]
      dimension = 1
      repeat_count = 2

      # Transforms:
      #   "layer0.weight": [[1, 2], [3, 4]]
      # Into:
      #   "layer0.weight": [[1, 1, 2, 2], [3, 3, 4, 4]]

  Args:
      target_keys: Sequence of keys to repeat.
      dimension: The axis/dimension to repeat along.
      repeat_count: Number of times to repeat elements.

  Returns:
      A Transformation function.
  """

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

    missing_keys = [k for k in target_keys if k not in result]
    if missing_keys:
      logging.warning(
          "Could not repeat keys %s. They were not found in params.",
          missing_keys,
      )

    for k in target_keys:
      if k in result:
        result[k] = _repeat_val(result[k], dimension, repeat_count)

    return result

  return transform

