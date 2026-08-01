
def fuse_by_keys(
    *,
    source_keys: Sequence[str],
    target_key: str,
    axis: int = 0,
) -> Transformation:
  """Fuses a specific set of source keys into a single target key.

  Example::
      source_keys = ["layer0.gate", "layer0.up"]
      target_key = "layer0.gate_up"

      # Transforms:
      #   "layer0.gate": arr1
      #   "layer0.up": arr2
      # Into:
      #   "layer0.gate_up": jnp.concatenate([arr1, arr2])

  Args:
      source_keys: Ordered sequence of keys to find and concatenate.
      target_key: The replacement key for the fused key.
      axis: Axis to concatenate along.

  Returns:
      A Transformation function.
  """

  def transform(
      *params: types.PyTreeOf[jax.Array],
  ) -> types.PyTreeOf[jax.Array]:
    if len(params) > 1:
      raise ValueError(
          "Can only fuse parameters in a single parameter structure."
      )
    params = params[0]
    result = dict(params)
    del params
    found_keys = [k for k in source_keys if k in result]
    if len(found_keys) == len(source_keys):
      _fuse_keys(result, source_keys, target_key, axis)
    elif found_keys:
      logging.warning(
          "Could not fuse %s. Found keys: %s, expected: %s",
          target_key,
          found_keys,
          source_keys,
      )

    return result

  return transform

