
def _normalize_structure(obj):
  if isinstance(obj, _ValueRepresentation):
    return obj
  if isinstance(obj, (tuple, list)):
    return tuple(map(_normalize_structure, obj))
  elif isinstance(obj, Mapping):
    return {
      _normalize_structure(k): _normalize_structure(v) for k, v in obj.items()
    }
  elif dataclasses.is_dataclass(obj):
    return {
      f.name: _normalize_structure(getattr(obj, f.name))
      for f in dataclasses.fields(obj)
    }
  elif isinstance(obj, enum.Enum):
    # `yaml.safe_dump` does not support Enum key types so extract the underlying value
    return obj.value
  else:
    return obj

