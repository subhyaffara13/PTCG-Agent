from typing import Any, Dict, Union

def _flatten_dict(space: Dict, x: dict[str, Any]) -> dict[str, Any] | NDArray[Any]:
    if space.is_np_flattenable:
        return np.concatenate(
            [np.array(flatten(s, x[key])) for key, s in space.spaces.items()]
        )
    return {key: flatten(s, x[key]) for key, s in space.spaces.items()}


def _flatten_dict(space, x) -> Union[dict, np.ndarray]:
    if space.is_np_flattenable:
        return np.concatenate([flatten(s, x[key]) for key, s in space.spaces.items()])
    return OrderedDict((key, flatten(s, x[key])) for key, s in space.spaces.items())


def _flatten_dict(input_dict, parent_key='', sep='.'):
  """Flattens and simplifies dict such that it can be used by hparams.

  Args:
    input_dict: Input dict, e.g., from ConfigDict.
    parent_key: String used in recursion.
    sep: String used to separate parent and child keys.

  Returns:
   Flattened dict.
  """
  items = []
  for k, v in input_dict.items():
    new_key = parent_key + sep + k if parent_key else k

    # Valid types according to https://github.com/tensorflow/tensorboard/blob/1204566da5437af55109f7a4af18f9f8b7c4f864/tensorboard/plugins/hparams/summary_v2.py
    valid_types = (
      bool,
      int,
      float,
      str,
      np.bool_,
      np.integer,
      np.floating,
      np.character,
    )

    if isinstance(v, dict):
      # Recursively flatten the dict.
      items.extend(_flatten_dict(v, new_key, sep=sep).items())
      continue
    elif not isinstance(v, valid_types):
      # Cast any incompatible values as strings such that they can be handled by hparams
      v = str(v)
    items.append((new_key, v))
  return dict(items)

