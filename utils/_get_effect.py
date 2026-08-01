
def _get_effect(op: _op_identifier) -> _EffectType | None:
    qualname = _get_op_qualname(op)
    entry = torch._library.simple_registry.singleton.find(qualname)
    return entry.effect.effect

