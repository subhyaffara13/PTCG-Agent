
def _mutable_mapping_set_key(
  x: tp.MutableMapping[Key, tp.Any], key: Key, value: tp.Any
):
  x[key] = value

