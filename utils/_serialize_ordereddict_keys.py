import json

def _serialize_ordereddict_keys(keys):
  if isinstance(keys, Sequence) and all(isinstance(k, str) for k in keys):
    return json.dumps(keys).encode("utf-8")
  else:
    raise NotImplementedError(
        "Serialization of collections.OrderedDict is supported only when the "
        f"keys are strings. Found keys: {keys}.")

