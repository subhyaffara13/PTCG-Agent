
def _map_keys_fn(fn):
  def map_fn(nested_dict):
    return {
        k: map_fn(v) if isinstance(v, dict) else fn(k, v)
        for k, v in nested_dict.items()
    }

  return map_fn


def _map_keys_fn(fn):
  def map_fn(nested_dict):
    return {
        k: map_fn(v) if isinstance(v, dict) else fn(k, v)
        for k, v in nested_dict.items()
    }

  return map_fn

