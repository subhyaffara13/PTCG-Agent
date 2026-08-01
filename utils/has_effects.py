
def has_effects(op) -> bool:
    return (
        isinstance(op, (torch._ops.HigherOrderOperator, torch._ops.OpOverload))
        and not has_aliasing(op)
        and _get_effect(op) is not None
    )


def has_effects(eqn: JaxprEqn) -> bool:
  effs = {e for e in eqn.effects if not dceable_effects.contains(e)}
  return bool(effs)

