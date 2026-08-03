import logging
import re

def fuse_by_pattern(
    *,
    pattern: str,
    unique_parts: Sequence[str],
    fused_unique_part: str,
    axis: int = 0,
) -> Transformation:
  r"""Fuses parameters by finding sets that match a pattern.

  Example:
      pattern = r"^(.*)\.(gate_proj|up_proj)\.weight$"
      unique_parts = ["gate_proj", "up_proj"]
      fused_unique_part = "gate_up_proj"

        Transforms:
          "model.layers.0.gate_proj.weight": arr1
          "model.layers.0.up_proj.weight": arr2
        Into:
          "model.layers.0.gate_up_proj.weight": jnp.concatenate([arr1, arr2])

  Args:
      pattern: Regex to filter keys that are candidates for fusing.
      unique_parts: Ordered sequence of unique parts to find and concatenate.
      fused_unique_part: The replacement unique part for the fused key.
      axis: Axis to concatenate along.

  Returns:
      A Transformation function.
  """
  compiled_pattern = re.compile(pattern)
  unique_regex = "|".join([re.escape(p) for p in unique_parts])
  compiled_unique = re.compile(unique_regex)

  def transform(
      *params: types.PyTreeOf[jax.Array],
  ) -> types.PyTreeOf[jax.Array]:
    if len(params) > 1:
      raise ValueError(
          "Can only fuse parameters in a single parameter structure."
      )
    params = params[0]
    groups = collections.defaultdict(dict)

    for key in params:
      if not compiled_pattern.match(key):
        continue
      match_unique = compiled_unique.search(key)
      if not match_unique:
        continue

      fused_key = compiled_unique.sub(lambda _: fused_unique_part, key)
      unique_part = match_unique.group(0)
      if unique_part in unique_parts:
        groups[fused_key][unique_part] = key

    result = dict(params)
    del params
    for fused_key, unique_dict in groups.items():
      if len(unique_dict) == len(unique_parts):
        keys_to_fuse = [unique_dict[p] for p in unique_parts]
        _fuse_keys(result, keys_to_fuse, fused_key, axis)
      else:
        logging.warning(
            "Could not fuse %s. Found parts: %s, expected: %s",
            fused_key,
            list(unique_dict.keys()),
            unique_parts,
        )

    return result

  return transform

