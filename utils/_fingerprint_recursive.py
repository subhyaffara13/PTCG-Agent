from typing import Any

def _fingerprint_recursive(
  obj: Any, path: tuple[str, ...], seen_modules: dict[FlaxId, int]
) -> Any:
  """Creates a hashable representation for a Module by traversing its structure recursively."""

  def _get_fingerprint(name: str, value: Any) -> tuple[str, Any]:
    return name, _fingerprint_recursive(value, (*path, name), seen_modules)

  if isinstance(obj, str):
    return obj
  elif hasattr(obj, '__fn_or_cls__'):  # support PaxConfig objects
    return _fingerprint_recursive(obj.__fn_or_cls__, path, seen_modules)
  elif isinstance(obj, Module):
    fingerprint: Any
    if obj._id in seen_modules:
      # if we have already seen the module we just use the index
      # as its static component
      fingerprint = seen_modules[obj._id]
      return type(obj), fingerprint
    else:
      # if its a new module we add it to the cache and give it
      # a new index
      seen_modules[obj._id] = len(seen_modules)
      # TODO(cgarciae): define a way for the user of nn.jit to define
      # what fields it wants to ignore per Module instance.
      fingerprints = []
      for field in dataclasses.fields(obj):
        if not hasattr(obj, field.name):
          continue
        if field.name not in ('parent', 'name'):
          value = getattr(obj, field.name)
          fingerprints.append(_get_fingerprint(field.name, value))
      # add state fingerprint
      state_fingerprint = (
        _get_fingerprint('in_compact_method', obj._state.in_compact_method),
        _get_fingerprint('in_setup', obj._state.in_setup),
        _get_fingerprint('setup_called', obj._state.setup_called),
        _get_fingerprint('is_initialized', obj._state.is_initialized),
        _get_fingerprint('autoname_cursor', obj._state.autoname_cursor),
      )
      fingerprints.append(('_state', state_fingerprint))
      # add scope fingerprint
      scope = obj.scope
      if scope is not None:
        static_scope = (
          _get_fingerprint('mutable', scope.mutable),
          _get_fingerprint('flags', scope.flags),
          _get_fingerprint('rng_counts', scope.rng_counters),
          _get_fingerprint('reservations', scope.reservations),
        )
        _check_field_is_hashable((*path, 'scope'), static_scope)
        fingerprints.append(('scope', static_scope))
      fingerprint = tuple(fingerprints)
      return type(obj), fingerprint
  elif dataclasses.is_dataclass(obj):
    fingerprints = []
    for field in dataclasses.fields(obj):
      if not hasattr(obj, field.name):
        continue
      value = getattr(obj, field.name)
      value_fingerprint = _get_fingerprint(field.name, value)
      fingerprints.append((field.name, value_fingerprint))
    return type(obj), tuple(fingerprints)
  elif isinstance(obj, core.DenyList):
    return type(obj), _get_fingerprint('deny', obj.deny)
  elif isinstance(obj, dict):
    fingerprint = tuple((k, _get_fingerprint(k, v)) for k, v in obj.items())
    return fingerprint
  elif serialization.is_serializable(obj):
    state = serialization.to_state_dict(obj)
    fingerprint = _fingerprint_recursive(state, path, seen_modules)
    return type(obj), fingerprint
  elif isinstance(obj, Mapping):
    return tuple((k, _get_fingerprint(k, v)) for k, v in obj.items())
  elif isinstance(obj, Iterable):
    return tuple(_get_fingerprint(str(i), v) for i, v in enumerate(obj))
  else:
    _check_field_is_hashable(path, obj)
    return obj

