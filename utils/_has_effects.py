
def _has_effects(effects) -> bool:
  not_really_effects = (core.NamedAxisEffect, core.InternalMutableArrayEffect)
  return any(not isinstance(e, not_really_effects) for e in effects)

