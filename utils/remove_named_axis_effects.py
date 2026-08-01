
def remove_named_axis_effects(
    jaxpr: Jaxpr, names: Collection[AxisName]
) -> Jaxpr:
  if not names or not jaxpr.effects:
    return jaxpr
  return jaxpr.replace(effects=filter_named_axis_effects(jaxpr.effects, names))

