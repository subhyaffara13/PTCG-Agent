
def filter_named_axis_effects(
    effects: Effects, names: Collection[AxisName]
) -> Effects:
  return {e for e in effects
          if not isinstance(e, NamedAxisEffect) or e.name not in names}

