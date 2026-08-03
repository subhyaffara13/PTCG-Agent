from typing import Any

def _restore_list(xs, state_dict: dict[str, Any]) -> list[Any]:
  if len(state_dict) != len(xs):
    raise ValueError(
      'The size of the list and the state dict do not match,'
      f' got {len(xs)} and {len(state_dict)} '
      f'at path {current_path()}'
    )
  ys = []
  for i in range(len(state_dict)):
    y = from_state_dict(xs[i], state_dict[str(i)], name=str(i))
    ys.append(y)
  return ys

